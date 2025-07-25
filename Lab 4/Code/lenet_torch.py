import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from torch.optim import SGD

# 1) Model definition
class LeNetReLU(nn.Module):
    def __init__(self, num_classes: int = 10):
        super(LeNetReLU, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, kernel_size=5)      # → (6, 28, 28)
        self.pool  = nn.MaxPool2d(2, 2)                  # → (6, 14, 14)
        self.conv2 = nn.Conv2d(6, 16, kernel_size=5)     # → (16, 10, 10)
        # pool → (16, 5, 5)
        self.fc1   = nn.Linear(16 * 5 * 5, 120)
        self.fc2   = nn.Linear(120, 84)
        self.fc3   = nn.Linear(84, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = F.relu(self.conv1(x))
        x = self.pool(x)
        x = F.relu(self.conv2(x))
        x = self.pool(x)
        x = x.view(x.size(0), -1)   # flatten to (batch, 16*5*5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)             # raw logits
        return x

# 2) Hyperparameters and setup
batch_size      = 64
test_batch_size = 1000
epochs          = 5
learning_rate   = 0.01
momentum        = 0.9
log_interval    = 200

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 3) Data transforms and loaders
transform = transforms.Compose([
    transforms.Resize(32),           # LeNet expects 32×32 inputs
    transforms.ToTensor(),           # → tensor in [0,1], shape C×H×W
    transforms.Normalize((0.1307,), (0.3081,))
])

train_dataset = datasets.MNIST(root="./data", train=True,  download=True, transform=transform)
test_dataset  = datasets.MNIST(root="./data", train=False, download=True, transform=transform)

train_loader  = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader   = DataLoader(test_dataset,  batch_size=test_batch_size, shuffle=False)

# 4) Instantiate model, loss, optimizer
model     = LeNetReLU(num_classes=10).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = SGD(model.parameters(), lr=learning_rate, momentum=momentum)

# 5) Training loop
def train():
    model.train()
    for epoch in range(1, epochs + 1):
        running_loss = 0.0
        for batch_idx, (data, target) in enumerate(train_loader, 1):
            data, target = data.to(device), target.to(device)
            optimizer.zero_grad()
            output = model(data)
            loss   = criterion(output, target)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            if batch_idx % log_interval == 0:
                avg = running_loss / log_interval
                print(f"Epoch {epoch} "
                      f"[{batch_idx * len(data)}/{len(train_loader.dataset)}]  "
                      f"Loss: {avg:.4f}")
                running_loss = 0.0

# 6) Testing loop
def test():
    model.eval()
    test_loss = 0.0
    correct   = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += criterion(output, target).item()
            pred = output.argmax(dim=1)
            correct += pred.eq(target).sum().item()

    test_loss /= len(test_loader)
    accuracy   = 100.0 * correct / len(test_loader.dataset)
    print(f"\nTest set: Average loss: {test_loss:.4f}, "
          f"Accuracy: {correct}/{len(test_loader.dataset)} "
          f"({accuracy:.2f}%)\n")

# 7) Run!
if __name__ == "__main__":
    train()
    test()
