import torch

def main():
    # 标量 (Scalar)
    a = 3.14  # 标量，单个数值
    print("标量 a:")
    print(a)
    print("---")

    # 向量 (Vector)
    a = torch.tensor([2, 4, 6])  # 向量，一维张量
    print("向量 a:")
    print(a)
    print("---")

    # 矩阵 (Matrix)
    A = torch.tensor([[1, 2], [3, 4]])  # 矩阵，二维张量
    print("矩阵 A:")
    print(A)
    print("---")

    # 张量 (Tensor)
    A = torch.randn(3, 32, 32)  # 三维张量，形状为 (3, 32, 32)
    print("张量 A:")
    print(A)
    print("---")

    # 集合 (Set)
    x1 = 1
    x2 = 2
    x3 = 3
    S = {x1, x2, x3}  # 集合，包含元素 x1, x2, x3
    print("集合 S:")
    print(S)
    print("---")

if __name__ == "__main__":
    main()