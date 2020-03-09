import torch
# a=torch.randn(2,2)
# print(a)


# x=torch.ones(1)
# print(x.data)
# print(x.data.requires_grad)
# y = 2 * x
# x.data *= 100 # 只改变了值，不会记录在计算图，所以不会影响梯度传播

# # y.backward()
# # print(x) # 更改data的值也会影响tensor的值
# # print(x.grad)
# z=2*x
# z.requires_grad_(True)
# c=2*z
# c.backward()
# print(c.grad_fn)
# print(z)
# print(z.grad)
x = torch.tensor(1.0, requires_grad=True)
y1 = x ** 2 
y1.retain_grad()
with torch.no_grad():
    y2 = x ** 3
y3 = y1 + y2

print(x.requires_grad)
print(y1, y1.requires_grad) # True
print(y2, y2.requires_grad) # False
print(y3, y3.requires_grad) # True

y3.backward()
print(x.grad)
print(y1.grad)

grads = {}
def save_grad(name):
    def hook(grad):
        grads[name] = grad
    return hook

x = torch.randn(1,1,requires_grad=True)
y = 3*x
z = y**2

# In here, save_grad('y') returns a hook (a function) that keeps 'y' as name
y.register_hook(save_grad('y'))
z.register_hook(save_grad('z'))
z.backward()

print(grads['y'])
print(grads['z'])