import csv
import random
class Homework4:

    # QUESTION 1
    # Implement randomized quicksort and heapsort in the below function
    # Input for the function - an array of floating point numbers ex: [3.0,9.0,1.0]
    # Output - sorted list of numbers ex: [1.0,3.0,9.0]
    # Numbers can be negative, repeated, and floating point numbers
    # DO NOT USE THE INBUILT HEAPQ MODULE TO SOLVE THE PROBLEMS
      
    def randomQuickSort(self, nums: list) -> list:

        def partition(arr, left, right): # Helper partition function that actually swaps elements to left and right of pivot once pivot is found. Uses Hoare's Partition
            x = arr[left] # Pivot value. Element against which all others are compared
            i = left # Left scan pointer. Moves rightward looking for elements >= pivot value
            j = right + 1 # Right scanning pointer. Moves leftward looking for elements <= pivot value. Allos first decrement before comparison begins
            while True:
                while True: # Move j left until arr[j] <= x
                    j -= 1
                    if arr[j] <= x: 
                        break
                while i < right and arr[i] < x:
                        i += 1 # Keeps moving i right until arr[i] >= x or boundary hit
                if i < j: # The two pointers haven't crossed yet, indicates misplaced pair, so we swap them 
                    arr[i], arr[j] = arr[j], arr[i] # Swap
                else:
                    return j

        def randomizedPartition(arr, left, right): # Helper randomizedPartition function to select random pivot and swap it with last element of array (right)
            p_index = random.randint(left, right) # Get random index from array range
            arr[left], arr[p_index] = arr[p_index], arr[left]  # Swap pivot to the beginning
            return partition(arr, left, right)

        def quickSortHelper(arr, left, right):
            if left < right:
                q = randomizedPartition(arr, left, right)
                quickSortHelper(arr, left, q)
                quickSortHelper(arr, q + 1, right)

        quickSortHelper(nums, 0, len(nums) - 1)
        return nums

    def heapSort(self,nums:list) -> list:
        
        def heapify(arr, n, i): # Helper function that heapifies arrays
            # Working with indices of values 
            left = 2*i+1 # Left child index
            right = 2*i+2 # Right child index
            maximus = i # Assume parent is largest then check children

            if left < n and arr[left] > arr[maximus]: # Left exists and it's greater than parent 
                maximus = left # Update indexes for later swap
            if right < n and arr[right] > arr[maximus]: # Right exists and it's greater than parent 
                maximus = right # Update....
            
            if maximus != i: # So i wasn't largest this means we have to swap the values in heap
                arr[i], arr[maximus] = arr[maximus], arr[i] # Actual swap happens only if parent wasn't max, after swap i will have the max value again
                heapify(arr, n, maximus) # Recursively recall heapify with index of smaller value to check with its subtree

        def buildMaxHeap(arr, n): # Helper function that build maxHeaps
            for i in range(n//2 - 1, -1, -1):  # Start from last non-leaf (n//2 - 1), work up to root
                heapify(arr, n, i)

        n = len(nums)
        buildMaxHeap(nums, n)
        
        for i in range(n-1, 0, -1):  # Shrink heap one by one
            nums[0], nums[i] = nums[i], nums[0]  # Move current max to end
            heapify(nums, i, 0)  # Restore heap on reduced array
        
        return nums

# Main Function
# Do not edit the code below
if __name__=="__main__":
    homework4  = Homework4()
    testCasesforSorting = []
    try:
        with open('testcases.csv','r') as file:
            testCases = csv.reader(file)
            for row in testCases:
                testCasesforSorting.append(row)
    except FileNotFoundError:
        print("File Not Found") 
    
    # Running Test Cases for Question 1
    print("RUNNING TEST CASES FOR QUICKSORT: ")
    
    for row , (inputValue,expectedOutput) in enumerate(testCasesforSorting,start=1):
        if(inputValue=="" and expectedOutput==""):
            inputValue=[]
            expectedOutput=[]
        else:
            inputValue=inputValue.split(" ")
            inputValue = [float(i) for i in inputValue]
            expectedOutput=expectedOutput.split(" ")
            expectedOutput = [float(i) for i in expectedOutput]
        actualOutput = homework4.randomQuickSort(inputValue)
        are_equal = all(x == y for x, y in zip(actualOutput, expectedOutput))
        if(are_equal):
            print(f"Test Case {row} : PASSED")
        else:
             print(f"Test Case {row}: Failed (Expected : {expectedOutput}, Actual: {actualOutput})")
    
    print("\nRUNNING TEST CASES FOR HEAPSORT: ")         
    for row , (inputValue,expectedOutput) in enumerate(testCasesforSorting,start=1):
        if(inputValue=="" and expectedOutput==""):
            inputValue=[]
            expectedOutput=[]
        else:
            inputValue=inputValue.split(" ")
            inputValue = [float(i) for i in inputValue]
            expectedOutput=expectedOutput.split(" ")
            expectedOutput = [float(i) for i in expectedOutput]
        actualOutput = homework4.heapSort(inputValue)
        are_equal = all(x == y for x, y in zip(actualOutput, expectedOutput))
        if(are_equal):
            print(f"Test Case {row} : PASSED")
        else:
             print(f"Test Case {row}: Failed (Expected : {expectedOutput}, Actual: {actualOutput})")

    # Script for Problem 3
    import time 
    import sys
    import tracemalloc

    # Notes: Python has max recursion limit of 1000
    # Heapsort time complexity is O(nlgn), this is because heapify takes O(lgn) and build-heap takes O(n)
    # Of the two time complexities the recursive part is in heapify so O(lgn) is what is to be considered
    # 10^8 is about 26 recursions so no problem with Heapsort
    # Quicksort is O(n) so recursion limit will need adjustment there

    # N sizes:
    powers = [4, 5, 6]  # Switched from 10^8 to just 10^6 cause 7 takes way too long
    arrays = []

    # Times
    quicksortTimes = []
    heapsortTimes = []

    # Memory
    quicksortMemory = []
    heapsortMemory = []

    for power in powers:
        N = 10**power # Setting N of numbers to get 

        # Making the arrays of random 10*N integers 
        ray = [random.uniform(-1000, 1000) for _ in range(N)] # Create list of N random ints
        arrays.append(ray) # Append that list to arrays

        sys.setrecursionlimit(N + 1000) # Set recursion limit to N + a buffer of 1000 more
        try:
            # Quicksort time measurements
            start = time.perf_counter() # Start timer
            homework4.randomQuickSort(ray.copy()) # Call for sorting algorithm (using copy so original ray for that N is unchanged for later tests)
            end = time.perf_counter() # End timer 
            quicksortTimes.append(end - start) # Record time

            # Quicksort memory measurements
            tracemalloc.start() # Start malloc tracing
            homework4.randomQuickSort(ray.copy()) # Call for sorting algorithm 
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop() # End malloc tracing
            quicksortMemory.append(peak) # Record malloc tracing of peak for comparisons (highest amount of memory recorded when using this algorithm)

            # Heapsort time measurements
            start = time.perf_counter() # Start timer
            homework4.heapSort(ray.copy()) # Call for sorting algorithm 
            end = time.perf_counter() # End timer 
            heapsortTimes.append(end - start) # Record time

            # Heapsort memory measurments
            tracemalloc.start() # Start malloc tracing
            homework4.heapSort(ray.copy()) # Call for sorting algorithm 
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop() # End malloc tracing
            heapsortMemory.append(peak) # Record malloc tracing

            print(f"{N} done.") # Debug
        except RecursionError:
            print(f"Recursion error at N = {N}")
            quicksortTimes.append(None)
            quicksortMemory.append(None)
            heapsortTimes.append(None)
            heapsortMemory.append(None)

    for i, power in enumerate(powers):
        N = 10**power
        print(f"\nN = 10^{power} ({N} elements)")
        print(f"  Quicksort  | Time: {quicksortTimes[i]:.4f}s | Memory: {quicksortMemory[i] / 1024:.2f} KB") # Divided by 1024 to convert from bytes to KB
        print(f"  Heapsort   | Time: {heapsortTimes[i]:.4f}s | Memory: {heapsortMemory[i] / 1024:.2f} KB")

    import matplotlib.pyplot as plt

    N_values = [10**4, 10**5, 10**6]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Quicksort vs Heapsort Performance", fontsize=14)

    # Time plot
    ax1.plot(N_values, quicksortTimes, marker='o', label='Quicksort')
    ax1.plot(N_values, heapsortTimes, marker='o', label='Heapsort')
    ax1.set_xscale('log')
    ax1.set_xlabel('N (log scale)')
    ax1.set_ylabel('Time (seconds)')
    ax1.set_title('Running Time')
    ax1.legend()
    ax1.grid(True)

    # Memory plot
    qs_mem_kb = [m / 1024 for m in quicksortMemory]
    hs_mem_kb = [m / 1024 for m in heapsortMemory]
    ax2.plot(N_values, qs_mem_kb, marker='o', label='Quicksort')
    ax2.plot(N_values, hs_mem_kb, marker='o', label='Heapsort')
    ax2.set_xscale('log')
    ax2.set_xlabel('N (log scale)')
    ax2.set_ylabel('Peak Memory (KB)')
    ax2.set_title('Peak Memory Usage')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig('sorting_performance.png')
    plt.show()
    
        


