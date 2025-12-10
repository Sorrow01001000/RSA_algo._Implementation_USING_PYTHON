import random

class RSA:
    def __init__(self):
        self.public_key = None
        self.private_key = None

    def gcd(self, a, b):
        """Calculates the Greatest Common Divisor."""
        while b != 0:
            a, b = b, a % b
        return a

    def multiplicative_inverse(self, e, phi):
        """Extended Euclidean Algorithm."""
        d = 0
        x1 = 0
        x2 = 1
        y1 = 1
        temp_phi = phi
        
        while e > 0:
            temp1 = temp_phi // e
            temp2 = temp_phi - temp1 * e
            temp_phi = e
            e = temp2
            
            x = x2 - temp1 * x1
            y = d - temp1 * y1
            
            x2 = x1
            x1 = x
            d = y1
            y1 = y
        
        if temp_phi == 1:
            return d + phi

    def is_prime(self, num):
        """Simple primality test."""
        if num < 2: return False
        if num == 2: return True
        if num % 2 == 0: return False
        for i in range(3, int(num**0.5) + 1, 2):
            if num % i == 0:
                return False
        return True

    def generate_prime_candidate(self, min_val, max_val):
        """Generates a random prime number."""
        while True:
            n = random.randint(min_val, max_val)
            if self.is_prime(n):
                return n

    def generate_key_pair(self, key_size_approx=100):
        """Generates Public and Private keys."""
        p = self.generate_prime_candidate(key_size_approx, key_size_approx * 10)
        q = self.generate_prime_candidate(key_size_approx, key_size_approx * 10)
        while p == q:
            q = self.generate_prime_candidate(key_size_approx, key_size_approx * 10)

        n = p * q
        phi = (p - 1) * (q - 1)

        e = random.randrange(1, phi)
        while self.gcd(e, phi) != 1:
            e = random.randrange(1, phi)

        d = self.multiplicative_inverse(e, phi)

        self.public_key = (e, n)
        self.private_key = (d, n)
        
        return self.public_key, self.private_key

    def encrypt(self, message, pub_key):
        """Encrypts string to list of integers."""
        e, n = pub_key
        encrypted_msg = []
        for char in message:
            m = ord(char)
            c = pow(m, e, n)
            encrypted_msg.append(c)
        return encrypted_msg

    def decrypt(self, encrypted_msg, priv_key):
        """Decrypts list of integers to string."""
        d, n = priv_key
        decrypted_msg = ""
        for num in encrypted_msg:
            m = pow(num, d, n)
            decrypted_msg += chr(m)
        return decrypted_msg

# --- Main Execution Block with Menu ---
if __name__ == "__main__":
    rsa = RSA()
    
    print("--- RSA System Starting ---")
    print("Generating new Key Pair for this session...")
    pub, priv = rsa.generate_key_pair(key_size_approx=1000)
    print("Keys generated successfully.")
    print(f"DEBUG info: Public Key: {pub}")

    while True:
        print("\n-------------------------")
        print("       MAIN MENU")
        print("-------------------------")
        print("1. Encrypt a message")
        print("2. Decrypt a message")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            msg = input("Enter the message to encrypt: ")
            cipher = rsa.encrypt(msg, pub)
            print(f"\n[SUCCESS] Encrypted Output (copy these numbers):")
            # Print as a comma-separated list for easier copying
            print(", ".join(map(str, cipher)))
            
        elif choice == '2':
            print("Enter the cipher numbers separated by commas (e.g., 1234, 5678):")
            cipher_input = input("> ")
            try:
                # Convert string input "123, 456" into list of ints [123, 456]
                cipher_list = [int(x.strip()) for x in cipher_input.split(',')]
                plain_text = rsa.decrypt(cipher_list, priv)
                print(f"\n[SUCCESS] Decrypted Message: {plain_text}")
            except ValueError:
                print("\n[ERROR] Invalid input. Please enter numbers separated by commas.")
            except Exception as e:
                print(f"\n[ERROR] Decryption failed: {e}")
                
        elif choice == '3':
            print("Exiting program. Goodbye!")
            break
        else:
            print("\n[INVALID] Please choose 1, 2, or 3.")