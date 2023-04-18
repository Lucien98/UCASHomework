import numpy as np                             # for fast array manipulation
import torch                                   # Pytorch
import torchvision                             # contains image datasets and many functions to manipulate images
import torchvision.transforms as transforms    # to normalize, scale etc the dataset
from torch.utils.data import DataLoader        # to load data into batches (for SGD)
from torchvision.utils import make_grid        # Plotting. Makes a grid of tensors
from torchvision.datasets import MNIST         # the classic handwritten digits dataset
import matplotlib.pyplot as plt                # to plot our images
import torch.nn as nn                          # Class that implements a model (such as a Neural Network)
import torch.nn.functional as F                # contains activation functions, sampling layers and more "functional" stuff
import torch.optim as optim                    # For optimization routines such as SGD, ADAM, ADAGRAD, etc

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)

batch_size = 100      # How many images to use for a SGD update
L = 1                 # Samples per data point. 
e_hidden = 500        # Number of hidden units in the encoder. 
d_hidden = 500        # Number of hidden units in the decoder. 
latent_dim = 2        
learning_rate = 0.001 # For SGD
weight_decay = 1e-5   # For SGD
epochs = 10          # Number of sweeps through the whole dataset, also called epochs

t = transforms.Compose([
                        transforms.ToTensor()
])

trainset = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=t)
testset  = torchvision.datasets.MNIST(root='./data', train=False, download=True, transform=t)

trainloader = DataLoader(trainset, batch_size=batch_size, shuffle=True)
testloader  = DataLoader(testset, batch_size=batch_size, shuffle=True)

with torch.no_grad():      
  images, targets = iter(trainloader).next()
  images = images.cpu()
  images = images.clamp(0, 1)
  images = images[:50]
  images_grid = make_grid(images, 10, 5)
  images_grid = images_grid.numpy()
  images_grid = np.transpose(images_grid, (1, 2, 0))
  plt.imshow(images_grid)
  plt.savefig('image/visualize-images.png')

class Encoder(nn.Module):
  def __init__(self):
    super(Encoder, self).__init__()
    self.hidden = nn.Linear(in_features=28*28, out_features=e_hidden)
    self.mu_layer     = nn.Linear(in_features=e_hidden, out_features=latent_dim)
    self.logvar_layer = nn.Linear(in_features=e_hidden, out_features=latent_dim)
    
  def forward(self, x):
    x = F.relu(self.hidden(x))
    return self.mu_layer(x), self.logvar_layer(x)

class Decoder(nn.Module):
  def __init__(self):
    super(Decoder, self).__init__()
    self.hidden = nn.Linear(in_features=latent_dim, out_features=d_hidden)
    self.output_layer = nn.Linear(in_features=d_hidden, out_features=28*28)

  def forward(self, z):
    z = F.relu(self.hidden(z))
    return torch.sigmoid(self.output_layer(z))

class VAE(nn.Module):
  def __init__(self):
    super(VAE, self).__init__()
    self.encoder = Encoder()
    self.decoder = Decoder()

  def sample_latent(self, mu, logvar):
    if self.training:
      eps = torch.randn_like(mu)
      return eps.mul(torch.exp(0.5*logvar)).add_(mu)
    else:   # This is used when testing 
      return mu    

  def forward(self, x):
    latent_mu, latent_logvar = self.encoder(x.view(-1, 28*28))
    z = self.sample_latent(latent_mu, latent_logvar)
    return self.decoder(z), latent_mu, latent_logvar   

def vae_loss(image, reconstruction, mu, logvar):
    reconstruction_loss = F.binary_cross_entropy(input=reconstruction.view(-1, 28*28), target=image.view(-1, 28*28), reduction='sum')
    kl = 0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    return reconstruction_loss - kl

vae = VAE()

vae = vae.to(device)

optimizer = optim.Adam(params=vae.parameters(), lr=learning_rate, weight_decay=weight_decay)

vae.train()

losses = []

for epoch in range(epochs):
  losses.append(0)

  number_of_batches = 0

  for images, _ in trainloader:
    images = images.to(device)

    optimizer.zero_grad()

    reconstructions, latent_mu, latent_logvar = vae(images)

    loss = vae_loss(images, reconstructions, latent_mu, latent_logvar)

    loss.backward()

    optimizer.step()

    losses[-1] += loss.item()        #.item() grabs the value in a tensor with only 1 value
    number_of_batches += 1
  
  losses[-1] /= number_of_batches
  print('Epoch [%d / %d] average reconstruction error: %f' % (epoch+1, epochs, losses[-1]))    

fig = plt.figure()
plt.plot(losses)
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.show()

plt.savefig('image/loss.png')

vae.eval()

test_loss, number_of_batches = 0.0, 0

for test_images, _ in testloader:

  with torch.no_grad():

    test_images = test_images.to(device)

    reconstructions, latent_mu, latent_logvar = vae(test_images)

    loss = vae_loss(test_images, reconstructions, latent_mu, latent_logvar)

    test_loss += loss.item()
    number_of_batches += 1

test_loss /= number_of_batches
print('average reconstruction error: %f' % (test_loss))

with torch.no_grad():
  print("Original Images")
  test_images = test_images.cpu()
  test_images = test_images.clamp(0, 1)
  test_images = test_images[:50]
  test_images = make_grid(test_images, 10, 5)
  test_images = test_images.numpy()
  test_images = np.transpose(test_images, (1, 2, 0))
  plt.imshow(test_images)
  plt.savefig('image/ori-image.png')

with torch.no_grad():
  print("Reconstructions")
  reconstructions = reconstructions.view(reconstructions.size(0), 1, 28, 28)
  reconstructions = reconstructions.cpu()
  reconstructions = reconstructions.clamp(0, 1)
  reconstructions = reconstructions[:50]
  plt.imshow(np.transpose(make_grid(reconstructions, 10, 5).numpy(), (1, 2, 0)))
  plt.savefig('image/recon-image.png')

vae.eval()
with torch.no_grad():
  z = torch.randn(50, latent_dim, device=device)

  recon_images = vae.decoder(z)
  recon_images = recon_images.view(recon_images.size(0), 1, 28, 28)
  recon_images = recon_images.cpu()
  recon_images = recon_images.clamp(0, 1)

  plt.imshow(np.transpose(make_grid(recon_images, 10, 5).numpy(), (1, 2, 0)))
  plt.savefig('image/data-gen.png')

with torch.no_grad():
  latent_x = np.linspace(-1.5, 1.5, 20)
  latent_y = np.linspace(-1.5, 1.5, 20)
  latents = torch.FloatTensor(len(latent_x), len(latent_y), 2)
  for i, lx in enumerate(latent_x):
    for j, ly in enumerate(latent_y):
      latents[j, i, 0] = lx
      latents[j, i, 1] = ly
  latents = latents.view(-1, 2)
  latents = latents.to(device)
  reconstructions = vae.decoder(latents).reshape(-1, 1, 28,28)
  reconstructions = reconstructions.cpu()
  fig, ax = plt.subplots(figsize=(10, 10))
  plt.imshow(np.transpose(make_grid(reconstructions.data[:400], 20, 20).clamp(0, 1).numpy(), (1, 2, 0))) 
  plt.savefig('image/latent-space.png')
