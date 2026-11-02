class Contact:
    '''
    Contact class to represent a contact with a name and number.
    Attributes:
        name (str): The name of the contact.
        number (str): The phone number of the contact.
    '''
 
    def __init__(self, name, number):
        self.name = name
        self.number = number
 
    def __str__(self):
        return f"{self.name}: {self.number}"
 
 
class Node:
    '''
    Node class to represent a single entry in the hash table.
    Attributes:
        key (str): The key (name) of the contact.
        value (Contact): The value (Contact object) associated with the key.
        next (Node): Pointer to the next node in case of a collision.
    '''
 
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
 
 
class HashTable:
    '''
    HashTable class to represent a hash table for storing contacts.
    Attributes:
        size (int): The size of the hash table.
        data (list): The underlying array to store linked lists for collision handling.
    Methods:
        hash_function(key): Converts a string key into an array index.
        insert(key, value): Inserts a new contact into the hash table.
        search(key): Searches for a contact by name.
        print_table(): Prints the structure of the hash table.
    '''
 
    def __init__(self, size):
        self.size = size
        self.data = [None] * size
 
    def hash_function(self, key):
        total = 0
        for char in key:
            total += ord(char)
        return total % self.size
 
    def insert(self, key, number):
        index = self.hash_function(key)
        current = self.data[index]
 
        while current is not None:
            if current.key == key:
                current.value.number = number
                return
            current = current.next
 
        new_node = Node(key, Contact(key, number))
        if self.data[index] is None:
            self.data[index] = new_node
        else:
            current = self.data[index]
            while current.next is not None:
                current = current.next
            current.next = new_node
 
    def search(self, key):
        index = self.hash_function(key)
        current = self.data[index]
 
        while current is not None:
            if current.key == key:
                return current.value
            current = current.next
 
        return None
 
    def print_table(self):
        for index in range(self.size):
            current = self.data[index]
            if current is None:
                print(f"Index {index}: Empty")
            else:
                line = f"Index {index}: "
                while current is not None:
                    line += f"- {current.value} "
                    current = current.next
                print(line)
 
 
# Test your hash table implementation here.
if __name__ == "__main__":
    table = HashTable(10)
    table.print_table()
 
    # Add some values
    table.insert("John", "909-876-1234")
    table.insert("Rebecca", "111-555-0002")
    print()
    table.print_table()
 
    # Search for a value
    contact = table.search("John")
    print("\nSearch result:", contact)
 
    # Edge Case #1 - Hash Collisions
    table.insert("Amy", "111-222-3333")
    table.insert("May", "222-333-1111")
    print()
    table.print_table()
 
    # Edge Case #2 - Duplicate Keys
    table.insert("Rebecca", "999-444-9999")
    print()
    table.print_table()
 
    # Edge Case #3 - Searching for a value not in the table
    print(table.search("Chris"))
 
 
'''
DESIGN MEMO
 
A hash table is the right structure for fast lookups because it turns a key
directly into an array index. Instead of scanning every contact one by one, the
hash function converts a name into a position, and the program jumps straight to
that spot. With a reasonably sized table and evenly spread keys, insert and
search take about O(1) time on average, no matter how many contacts are stored.
That is why phone contact lists feel instant even with thousands of entries.
 
I handled collisions with separate chaining. Each slot in the array holds either
None or the head of a linked list of Node objects. When two names hash to the
same index, such as "Amy" and "May", the new node is added to the end of that
index's list. During insert, I walk the chain first to check whether the name
already exists; if it does, I update the number instead of adding a duplicate.
Search works the same way: hash the name, then traverse only that one short
chain comparing keys, returning None if nothing matches.
 
An engineer might choose a hash table over a list or tree when the main
operations are looking up, inserting, or updating items by an exact key and
speed matters more than order. A list needs O(n) scanning to find a name, and a
balanced tree needs O(log n) but keeps data sorted, which only matters for range
queries or ordered output. The tradeoff is that a hash table does not keep
sorted order, and performance degrades if the table is too small or the hash
function clusters keys.
'''