

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1  # 未找到

if __name__ == "__main__":
    data = [1, 3, 5, 7, 9, 11, 13, 15]
    target1 = 7
    target2 = 4

    index1 = binary_search(data, target1)
    index2 = binary_search(data, target2)

    print(f"查找 {target1} 的结果: {index1}")
    print(f"查找 {target2} 的结果: {index2}")