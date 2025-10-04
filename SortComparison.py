


"""
Sorting comparison demo in Python.
We benchmark several classic sorting algorithms on the same random data
and print how long each one takes. Comments are intentionally informal
to make the code easier to read.
"""

import random
import copy
import time

#
# Bubble Sort: This is mainly used for teaching purposes and is almost never used in real-world code.
# It's very simple and easy to understand, but extremely slow for large datasets.
# Only use this if you want to demonstrate how sorting works step by step.
# It works by repeatedly swapping adjacent out-of-order elements until the whole list is sorted.
def bubble_sort(arr):
    n = len(arr)
    # After each pass, the largest element "bubbles" to the end.
    for i in range(n):
        for j in range(0, n - i - 1):
            # If current item is bigger than the next one, swap them.
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

#
# Merge Sort: Use this when you need stable sorting and guaranteed O(n log n) performance, even in the worst case.
# It's great for sorting large datasets, can be parallelized, and works well for external sorting (e.g., sorting data on disk).
# Merge sort splits the list, sorts each half, then merges them back in order.
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]
        # Recursively sort the left and right halves.
        merge_sort(L)
        merge_sort(R)
        i = j = k = 0
        # Merge the two sorted halves back into arr.
        while i < len(L) and j < len(R):
            if L[i] < R[j]:  # Take the smaller head element first
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        # Copy any leftovers from L
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        # Copy any leftovers from R
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

#
# Quick Sort (in-place version): This is usually the fastest sorting algorithm on average for in-memory arrays.
# This version sorts the array in place, which is more memory efficient and closer to how real-world quicksort is implemented.
# It uses the Lomuto partition scheme.
def partition(arr, low, high):
    # Lomuto partition: pick the last element as pivot
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quick_sort_inplace(arr, low, high):
    # Conversational: This is the in-place quick sort version, more memory efficient, and closer to what real-world libraries use.
    if low < high:
        pi = partition(arr, low, high)
        # Recursively sort elements before and after partition
        quick_sort_inplace(arr, low, pi - 1)
        quick_sort_inplace(arr, pi + 1, high)

#
# Insertion Sort: This is a great choice for very small arrays or arrays that are already nearly sorted.
# It's simple and has low overhead, so it's often used as a base case in hybrid sorting algorithms.
# It works by taking the next item and inserting it into the sorted left side.
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        # Shift larger items on the left to the right
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        # Place the key in its correct spot
        arr[j + 1] = key

#
# Heap Sort: Use this when you need guaranteed O(n log n) performance and want to sort in place with minimal extra memory.
# It's good when memory is tight, but it's usually a bit slower than quick sort or merge sort in practice.
# Heap sort builds a max-heap, then repeatedly moves the max element to the end.
def heapify(arr, n, i):
    # Find the largest among root, left child, and right child
    largest = i
    l = 2 * i + 1  # Left child index
    r = 2 * i + 2  # Right child index
    if l < n and arr[l] > arr[largest]:
        largest = l
    if r < n and arr[r] > arr[largest]:
        largest = r
    # If the largest isn't the parent, swap and continue heapifying
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)
    # Build a max-heap (rearrange array)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    # Extract elements one by one, moving max to the end
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)

if __name__ == "__main__":
    # Generate the same random data for all algorithms so it's a fair race.
    n = 20000
    data = [random.randint(0, 1000000) for _ in range(n)]

    # Use deep copies so each algorithm gets identical input.
    arr1 = copy.deepcopy(data)
    arr2 = copy.deepcopy(data)
    arr3 = copy.deepcopy(data)
    arr4 = copy.deepcopy(data)
    arr5 = copy.deepcopy(data)

    # Time bubble sort
    start = time.time()
    bubble_sort(arr1)
    end = time.time()
    # Convert seconds to milliseconds for easier reading.
    print("Bubble Sort time:", (end - start) * 1000, "ms")

    # Time merge sort
    start = time.time()
    merge_sort(arr2)
    end = time.time()
    print("Merge Sort time:", (end - start) * 1000, "ms")

    # Time quick sort (in-place version)
    start = time.time()
    quick_sort_inplace(arr3, 0, len(arr3) - 1)
    end = time.time()
    print("Quick Sort time:", (end - start) * 1000, "ms")

    # Time insertion sort
    start = time.time()
    insertion_sort(arr4)
    end = time.time()
    print("Insertion Sort time:", (end - start) * 1000, "ms")

    # Time heap sort
    start = time.time()
    heap_sort(arr5)
    end = time.time()
    print("Heap Sort time:", (end - start) * 1000, "ms")