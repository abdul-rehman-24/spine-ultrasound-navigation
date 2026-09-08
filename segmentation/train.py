"""3D U-Net training loop for binary spine segmentation.

Key lesson learned: plain DiceLoss gets stuck near Dice~0.10-0.15 due to
vanishing gradients on near-zero initial overlap. DiceCELoss (Dice + Cross
Entropy) resolves this reliably.
"""
import os
import torch
import pandas as pd
from monai.networks.nets import UNet
from monai.losses import DiceCELoss
from monai.metrics import DiceMetric
from monai.inferers import sliding_window_inference

from dataset import PATCH_SIZE


def build_model(device):
    return UNet(
        spatial_dims=3, in_channels=1, out_channels=1,
        channels=(16, 32, 64, 128, 256), strides=(2, 2, 2, 2), num_res_units=2,
    ).to(device)


def train(model, train_loader, val_loader, device, max_epochs=100,
          checkpoint_path="checkpoints/best_model.pth",
          log_path="results/metrics/train_log.csv",
          resume_best_metric=0.0):
    loss_function = DiceCELoss(sigmoid=True, lambda_dice=0.5, lambda_ce=0.5)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    dice_metric = DiceMetric(include_background=False, reduction="mean")

    os.makedirs(os.path.dirname(checkpoint_path), exist_ok=True)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    best_metric = resume_best_metric
    log = []

    for epoch in range(max_epochs):
        model.train()
        epoch_loss = 0
        for batch in train_loader:
            inputs, labels = batch["image"].to(device), batch["label"].to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = loss_function(outputs, labels)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
        epoch_loss /= len(train_loader)

        if (epoch + 1) % 5 == 0:
            model.eval()
            with torch.no_grad():
                for val_batch in val_loader:
                    val_inputs = val_batch["image"].to(device)
                    val_labels = val_batch["label"].to(device)
                    val_outputs = sliding_window_inference(val_inputs, PATCH_SIZE, 1, model)
                    val_outputs = (torch.sigmoid(val_outputs) > 0.5).float()
                    dice_metric(y_pred=val_outputs, y=val_labels)
                metric = dice_metric.aggregate().item()
                dice_metric.reset()
                print(f"Epoch {epoch+1}/{max_epochs} - Loss: {epoch_loss:.4f} - Val Dice: {metric:.4f}")
                log.append({"epoch": epoch + 1, "loss": epoch_loss, "val_dice": metric})
                if metric > best_metric:
                    best_metric = metric
                    torch.save(model.state_dict(), checkpoint_path)
        else:
            print(f"Epoch {epoch+1}/{max_epochs} - Loss: {epoch_loss:.4f}")

    pd.DataFrame(log).to_csv(log_path, index=False)
    print(f"Training complete. Best Val Dice: {best_metric:.4f}")
    return best_metric


def evaluate(model, test_loader, device, checkpoint_path="checkpoints/best_model.pth"):
    model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    model.eval()
    dice_metric = DiceMetric(include_background=False, reduction="mean")
    results = []
    with torch.no_grad():
        for i, batch in enumerate(test_loader):
            inputs, labels = batch["image"].to(device), batch["label"].to(device)
            outputs = sliding_window_inference(inputs, PATCH_SIZE, 1, model)
            outputs_bin = (torch.sigmoid(outputs) > 0.5).float()
            dice_metric(y_pred=outputs_bin, y=labels)
            dice_val = dice_metric.aggregate().item()
            dice_metric.reset()
            results.append(dice_val)
    return results
