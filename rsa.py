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
            
    def mod_exp(self, base, exp, mod):
        result = 1
        base = base % mod
        while exp > 0:
            if exp % 2 == 1:      
                result = (result * base) % mod
            base = (base * base) % mod
            exp //= 2
        return result       

    def generate_key_pair(self, key_size_approx=100):
        """Generates Public and Private keys."""
        p = self.generate_prime_candidate(key_size_approx, key_size_approx * 10)
        q = self.generate_prime_candidate(key_size_approx, key_size_approx * 10)

        self.p=p
        self.q=q

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
        encrypted_msg = ""
        for char in message:
            m = ord(char)
            c = self.mod_exp(m, e, n)
            # Split c into digits and convert each digit to a character
            # Add 100 to make it printable and not normal ASCII
            for digit in str(c):
                encrypted_msg += chr(int(digit) + 100)
                # Add a separator character to mark end of number
            encrypted_msg += chr(200)
        return encrypted_msg

    def decrypt(self, encrypted_msg, priv_key):
        """Decrypts list of integers to string."""
        d, n = priv_key
        decrypted_msg = ""
        c = 0

        for num in encrypted_msg:
            if ord(num) == 200:  # separator reached
                m = self.mod_exp(c, d, n)
                decrypted_msg += chr(m)
                c = 0   
            else:
                c = c * 1000 + (ord(num) - 100)

        return decrypted_msg

# --- Main Execution Block with Menu ---
if __name__ == "__main__":
    rsa = RSA()

    print("--- RSA System Starting ---")
    print("Generating new Key Pair for this session...")

    # Generate keys
    pub, priv = rsa.generate_key_pair(key_size_approx=1000)

    e, n = pub
    d, _ = priv

    # Print P and Q
    print("\n--- INTERNAL VALUES ---")
    print(f"p = {rsa.p}")
    print(f"q = {rsa.q}")
    print(f"n = {n}")
    print(f"phi = {(rsa.p - 1) * (rsa.q - 1)}")

    print("\n--- KEY INFORMATION ---")
    print(f"Public Key  (e, n): {pub}")
    print(f"Private Key (d, n): {priv}")

    # USER INPUT
    message = input("\nEnter a message to encrypt: ")

    # Encrypt & Decrypt
    encrypted = rsa.encrypt(message, pub)
    decrypted = rsa.decrypt(encrypted, priv)

    print("\n--- ENCRYPTION RESULT ---")
    print("Encrypted (as numbers):")
    print(", ".join(map(str, encrypted)))

    print("\n--- DECRYPTION RESULT ---")
    print(f"Decrypted text: {decrypted}")