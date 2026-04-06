# FEEL FREE TO ADD MORE FUNCTIONS AS PER YOUR NEED
# THERE IS NO UNCHANGEABLE "MAIN" FUNCTION IN THIS HW

import time
import random
import matplotlib.pyplot as plt

# Implement HashMap in this class
# Do not use built in dictionary
# Implement own hashing function using division/multiplication method
class HashMap:
    def __init__(self, size=101):
        self.size = size # Using size parameter for table size
        self.count = 0 # Track number of key-value pairs inserted for open addressing
        self.table = [None] * self.size # Each slot will store at most one key-value pair (None * size slots initially)
        self.load_factor_threshold = 0.7 # Factor to trigger dynamic resizing to keep performance up (when (self.count / self.size) > 0.7)
        self.DELETED = object() # Mark deleted slots for linear probing in open addressing
        self.last_probe_count = 0 # Counts number of probing steps done by search or insert. Set to 0 again inside each method and updated each iteration
        self.total_insert_probes = 0 # Total insert probes
        self.total_search_probes = 0 # Total search probes
        self.total_searches = 0 # Total searches
        # total isnert probes/count will yield average insert probes for a table
        # total search probes/total searcher will yield average search probes for a table
       
    # retrieve a value associated with the key
    def search(self,key): # Open addressing with linear probing
        self.last_probe_count = 0
        index = self._hash(key, "division") # Hash the key for index

        for i in range(self.size): # Open addressing liner probing
            self.total_search_probes += 1 # Increment total search probes
            self.last_probe_count += 1 # Increment probe count
            slot = self.table[index] # Slot with calculated index

            if slot is None: # Nothing being stored here interrupt loop
                self.total_searches += 1 # Update total searches
                return "Element doesn't exist"
            elif slot is not self.DELETED and slot[0] == key: # If slot isn't marked and key verify identity return value
                self.total_searches += 1 # Update total searches
                return slot[1]
            index = (index + 1) % self.size # Update index by 1

        self.total_searches += 1 # Total searches update
        return "Element doesn't exist" # Safety net in case map has no None (Could be filled and key isnt in there or just filled with DELETED)

    # insert the key value pair into the hash tables
    def insert(self,key,value):
        self.last_probe_count = 0
        index = self._hash(key, "division") # Create index
        first_deleted = None # To store first DELETED location

        for i in range(self.size): # Open addressing, linear probing
            self.total_insert_probes += 1 # Updare total insert probes
            self.last_probe_count += 1 # Increment probe count
            slot = self.table[index] # Slot....

            if slot is None: # If current slot is empty
                if first_deleted is not None: # If there was a deleted slot
                    self.table[first_deleted] = (key, value) # Use that deleted slot to store tuple
                else: # In this case there was no deleted slot
                    self.table[index] = (key, value) # Use this empty slot
                self.count += 1 # Update active key count
                if self.count / self.size > self.load_factor_threshold: # Trigger dynamic resizing
                    self.dynamicResizing()
                return # All good return
            
            elif slot is self.DELETED: # This slot is a deleted slot
                if first_deleted is None: # If this is the first deleted slot (meaning first deleted was None)
                    first_deleted = index # Store the deleted slot index
                    # Dont insert yet cause there may be a matching key after to update
            
            elif slot[0] == key: # Keys for this slot match
                self.table[index] = (key, value) # Update key's corresponding value
                return 
            
            index = (index + 1) % self.size # Update index by 1

        # After full probing, insert into first_deleted if it exists
        if first_deleted is not None: # We have a first deleted
            self.table[first_deleted] = (key, value) # Use that to store tuple
            self.count += 1 # Update active key count
            if self.count / self.size > self.load_factor_threshold: # Trigger dynamic resizing
                self.dynamicResizing()
            return 
        
        raise Exception("Hash table is full")

    # remove the key value pair from the hash table
    def delete(self,key):
        index = self._hash(key, "division")
        
        for i in range(self.size):
            slot = self.table[index] # self.table[index] is always first possible occurrence, the tuple we're looking for (assuming it exists)
            # is here or after the DELETED

            if slot is None:
                return "Key not found" # Safe to stop probing here: keys are never inserted beyond None slot (insert() handles this)
            elif slot is self.DELETED: # Slot is DELETED (This is the first possible position to check, then we keep iterating/probing past the deleted)
                pass # Keep probing
            elif slot[0] == key: # Keys match
                self.table[index] = self.DELETED  # Mark as deleted
                self.count -= 1 # Update count
                return "Key deleted"
            index = (index + 1) % self.size

        return "Key not found"


    # optional for open addressing collision method
    # if you choose chaining, don't forget to discuss it in the report
    def dynamicResizing(self):
        old_table = self.table
        self.size *= 2  # Double the size (or next prime for fewer collisions?)
        self.table = [None] * self.size
        self.count = 0  # Restart count

        for slot in old_table:
            if slot is not None and slot is not self.DELETED: # Slot is an active key
                self.insert(slot[0], slot[1])

    # hashing methods
    def _hash(self, key, method="division"): # Set method to division in the whole program

        # Input verification for key:
        if isinstance(key, int): # Key is an integer
            int_key = key
        elif isinstance(key, str): # Key is a string
            int_key = 0
            for c in key: # Loop through each character and convert to int
                int_key = (int_key * 31 + ord(c)) # Multiply by 31 (prime number to reduce collisions: Polynomial rolling hash thing) and add new characater's value 
        else: 
            raise TypeError("Unsupported key type") # Otherwise key type is trash

        if method == "division": # Implement division method
            return int_key % self.size
        elif method == "multiplication": # Implement multiplication method
            A = 0.6180339887  # Golden ratio fraction 
            return int(self.size * ((int_key * A) % 1)) # Cast to int, mutliplication hashing method
        else:
            raise ValueError("Unknown hash method") # Otherwise hashing method is trash

# Problem 2: Performance Analysis

def generate_keys(distribution, n):

    distribution = distribution.lower() # Set distribution name to lower for comparisons
    
    if distribution == "uniform": # uniform case
        return [random.randint(0, 10000) for _ in range(n)] 
    elif distribution == "skewed": # skewed case
        return [random.randint(0, 100) for _ in range(n)]
    elif distribution == "sequential": # sequential case
        return list(range(n))
    else:
        raise ValueError("Unknown distribution type")


def measure_search_time(hashmap, keys):
    total_time = 0
    sampled_keys = random.sample(keys, len(keys))  # all keys, random order, no repeats. Equivalent to getting a random index for key in keys to pick. 
    # If I used the latter tho, I'd have to make sure the random index wasnt used before otherwise I'd add time for the same key search multiple times
    # to the average

    for key in sampled_keys: # For each random key
        start = time.perf_counter() # Start timer
        hashmap.search(key) # Perform search
        end = time.perf_counter() # End timer
        total_time += (end - start) # Add up time

    return total_time / len(sampled_keys) # Return average search time of this hashmap, with these keys

def run_experiments():
    # test across different table sizes and load factors

    # Experiment's parameters
    table_sizes = [101, 211, 311] # 3 tables
    distributions = ["uniform", "skewed", "sequential"] # 3 dirstributions per table size
    n = 1000  # Total keys to generate
    batch_size = 50  # Insert this many keys at a time before measuring
    results = {} # Final return dictionary with all results

    for size in table_sizes:
        results[size] = {} # Create an empty dictionary at each key (size)
        for distribution in distributions:
            results[size][distribution] = { # Create entry inside that dictionary
                "load_factors": [],
                "search_times": [],
                "insert_probe_lengths": [],
                "search_probe_lengths": []
            }

            keys = generate_keys(distribution, n) # Generate 1000 keys per distribution
            new_map = HashMap(size) # New hashmap per distribution

            for batch_start in range(0, n, batch_size):  # 0, 50, 100, ... 950
                batch = keys[batch_start : batch_start + batch_size]  # 50 keys
                for key in batch: # At each batch
                    new_map.insert(key, key) # Insert keys
                # Befor loading new batch record results with last batch 
                results[size][distribution]["load_factors"].append(new_map.count/new_map.size) # Record load factor 
                non_existent = [random.randint(10001, 20000) for _ in range(batch_size)]  # Outside insert range. Onlys used to trigger unsuccessful searches
                mixed_keys = keys[:batch_start + batch_size] + non_existent # Mix the keys with non-existing keys
                results[size][distribution]["search_times"].append(measure_search_time(new_map, mixed_keys)) # Record avg search time
                results[size][distribution]["insert_probe_lengths"].append(new_map.total_insert_probes / new_map.count) # Record avg insert probe length
                results[size][distribution]["search_probe_lengths"].append(new_map.total_search_probes/new_map.total_searches) # Record avg search probe length
                # Measure_search_time is called before we record avg search probe length so it's safe.

    return results



def plot_results(results):
    table_sizes = list(results.keys()) # Top level keys of results are table sizes
    distributions = list(results[table_sizes[0]].keys()) # Get first table size then extract the distribution types

    # Plot 1: Load factor vs search time (one plot per distribution)
    for dist in distributions:
        plt.figure(figsize=(10, 5)) # New figure for each distribution
        for size in table_sizes: # One curve per table size on the same plot
            load_factors = results[size][dist]["load_factors"]
            search_times = results[size][dist]["search_times"]
            plt.plot(load_factors, search_times, label=f"Table size {size}")
        plt.title(f"Load Factor vs Search Time ({dist})")
        plt.xlabel("Load Factor")
        plt.ylabel("Average Search Time (s)")
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"load_vs_searchtime_{dist}.png")
        plt.show()

    # Plot 2: Load factor vs probe length (one plot per distribution)
    for dist in distributions:
        plt.figure(figsize=(10, 5))
        for size in table_sizes:
            load_factors = results[size][dist]["load_factors"]
            insert_probes = results[size][dist]["insert_probe_lengths"]
            search_probes = results[size][dist]["search_probe_lengths"]
            plt.plot(load_factors, insert_probes, label=f"Insert probes (size {size})", linestyle="--")
            plt.plot(load_factors, search_probes, label=f"Search probes (size {size})", linestyle="-")
        plt.title(f"Load Factor vs Probe Length ({dist})")
        plt.xlabel("Load Factor")
        plt.ylabel("Average Probe Length")
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"load_vs_probelength_{dist}.png")
        plt.show()

    # Plot 3: Distribution comparison (fixed table size 101)
    fixed_size = table_sizes[0]
    plt.figure(figsize=(10, 5)) # New figure for distribution comparison
    for dist in distributions: # One curve per distribution on the same plot
        load_factors = results[fixed_size][dist]["load_factors"]
        search_times = results[fixed_size][dist]["search_times"]
        plt.plot(load_factors, search_times, label=dist)
    plt.title(f"Search Time by Distribution (Table size {fixed_size})")
    plt.xlabel("Load Factor")
    plt.ylabel("Average Search Time (s)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("distribution_comparison.png")
    plt.show()


# Driver
if __name__ == "__main__":

    # Test
    hm = HashMap(11) # Initialize hashmap of size 11
    hm.insert("bike", 101)
    print("Insert probe count (bike):", hm.last_probe_count)
    hm.insert(99, 99) # int key case
    hm.insert("boat", 3)
    hm.table[5] = hm.DELETED # Deleted slot simulation
    hm.insert("platypus", 2)

    print(hm.search("platypus")) # Push search past deleted slot case
    print("Search probe count (platypus):", hm.last_probe_count)
    print(hm.search("yo")) # Element doesn't exist case
    print("Search probe count (yo - miss):", hm.last_probe_count)
    print(hm.search(99))
    print("Search probe count (99):", hm.last_probe_count)

    print("\n--- generate_keys tests ---")
    try:
        uniform_keys = generate_keys("uniform", 50)
        skewed_keys = generate_keys("SKEWED", 50)
        sequential_keys = generate_keys("sequential", 50)

        print(uniform_keys[:5])    # Preview first 5
        print(skewed_keys[:5])
        print(sequential_keys[:5])
        print(generate_keys("bad", 5))  # Should raise ValueError
    except ValueError as e:
        print(f"Error: {e}")

    print("\n--- measure_search_time tests ---")
    hm2 = HashMap(101)
    for k in uniform_keys:
        hm2.insert(k, k)
    print("Uniform:", measure_search_time(hm2, uniform_keys))

    hm3 = HashMap(101)
    for k in skewed_keys:
        hm3.insert(k, k)
    print("Skewed:", measure_search_time(hm3, skewed_keys))

    hm4 = HashMap(101)
    for k in sequential_keys:
        hm4.insert(k, k)
    print("Sequential:", measure_search_time(hm4, sequential_keys))

    print("\n--- probe count tests clean version ---")
    hm5 = HashMap(11)
    hm5.insert("bike", 1)
    print("Insert probe count:", hm5.last_probe_count)
    hm5.search("bike")
    print("Search hit probe count:", hm5.last_probe_count)
    hm5.search("nothere")
    print("Search miss probe count:", hm5.last_probe_count)

    print("\n--- Running experiments and plotting ---")
    results = run_experiments()
    plot_results(results)
