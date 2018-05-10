import torch
import pandas as pd
import numpy as np


class stair_net(torch.nn.Module):
	def __init__(self, D_in, H, D_out):
		super(stair_net, self).__init__()
		self.linear1 = torch.nn.Linear(D_in, H)
		self.linear2 = torch.nn.Linear(H, D_out)

	def forward(self, x):
		sigm = torch.nn.Sigmoid()
		h = self.linear1(x)
		h_sigm = sigm(h)
		y_pred = self.linear2(h_sigm)
		return y_pred

#dataset = np.read('/home/robert/csv_etc/mid_values.csv')
dataset = np.genfromtxt('/home/robert/csv_etc/mid_values.txt', delimiter =',')

#print(dataset[0])
#print(np.shape(dataset))
datatorch = torch.from_numpy(dataset).float()
#print(datatorch[0])
print(datatorch.shape)
train_x = torch.cat((datatorch[:142],datatorch[203:320]), 0)
test_x = torch.cat((datatorch[142:203],datatorch[320:369]), 0)

# N is batch size; D_in is input dimension;
# H is hidden dimension; D_out is output dimension.
N, D_in, H, D_out = 100, 376, 10, 1

# Create random Tensors to hold inputs and outputs
#x = torch.randn(N, D_in)
#y = torch.randn(N, D_out)

train_y = torch.ones(142, D_out)
train_y = torch.cat((train_y, torch.zeros(117, D_out)), 0)
test_y = torch.ones(61, D_out)
test_y = torch.cat((test_y, torch.zeros(49, D_out)), 0)

# Use the nn package to define our model as a sequence of layers. nn.Sequential
# is a Module which contains other Modules, and applies them in sequence to
# produce its output. Each Linear Module computes output from input using a
# linear function, and holds internal Tensors for its weight and bias.
#model = torch.nn.Sequential(
#    torch.nn.Linear(D_in, H),
#    torch.nn.Sigmoid(),
#    torch.nn.Linear(H, D_out),
#)
model = stair_net(D_in, H, D_out)
# The nn package also contains definitions of popular loss functions; in this
# case we will use Mean Squared Error (MSE) as our loss function.
loss_fn = torch.nn.MSELoss(size_average=False)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
#learning_rate = 1e-4
for t in range(4000):
    # Forward pass: compute predicted y by passing x to the model. Module objects
    # override the __call__ operator so you can call them like functions. When
    # doing so you pass a Tensor of input data to the Module and it produces
    # a Tensor of output data.
    y_pred = model(train_x)
    #if t%10 is 0:
      #print(y_pred[0])
    # Compute and print loss. We pass Tensors containing the predicted and true
    # values of y, and the loss function returns a Tensor containing the
    # loss.
    loss = loss_fn(y_pred, train_y)
    print(t, loss.item())

    # Zero the gradients before running the backward pass.
    #model.zero_grad()
    optimizer.zero_grad()


    # Backward pass: compute gradient of the loss with respect to all the learnable
    # parameters of the model. Internally, the parameters of each Module are stored
    # in Tensors with requires_grad=True, so this call will compute gradients for
    # all learnable parameters in the model.
    loss.backward()

    optimizer.step()
    # Update the weights using gradient descent. Each parameter is a Tensor, so
    # we can access and gradients like we did before.
    #with torch.no_grad():
    #    for param in model.parameters():
    #       param -= learning_rate * param.grad

y_test = model(test_x)
print(y_test)
print(test_y)
acc = test_y - y_test
print(acc)
stcorr=0
nocorr=0
incorr=0
for i in range(len(test_y)):
	if y_test[i] > 0.9 and test_y[i] == 1:
		stcorr = stcorr+1
	if y_test[i] < 0.3 and test_y[i] == 0:
		nocorr = nocorr+1 
	if((y_test[i] > 0.9) and (test_y[i] == 0)) or ((y_test[i] < 0.3) and (test_y[i] == 1)):
		incorr = incorr+1
print(len(test_y))
print("stairs correctly classified : %d" % (stcorr))
print("empty correctly classified : %d" % (nocorr))
print("incorrect classification : %d" % (incorr))

torch.save(model.state_dict(), 'testmodel.pt')