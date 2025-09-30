#!/usr/bin/env python3
"""
Password Cracker for HW2 Part 3
Cracks MD5 hashed passwords using brute force attack

Author: Showkot Hossain
Course: SSE Fall 2025
"""

import hashlib
import itertools
import string
import time
from typing import List, Set


class PasswordCracker:
    def __init__(self):
        # Define the character set as specified in the assignment
        self.charset = string.ascii_letters + string.digits + '&@#'  # a-z, A-Z, 0-9, &, @, #
        self.min_length = 3
        self.max_length = 6
        self.cracked_passwords = []
        
    def load_hashes(self, filename: str) -> Set[str]:
        """Load MD5 hashes from file"""
        hashes = set()
        try:
            with open(filename, 'r') as file:
                for line in file:
                    hash_value = line.strip()
                    if hash_value:  # Skip empty lines
                        hashes.add(hash_value.lower())
            print(f"Loaded {len(hashes)} hashes from {filename}")
        except FileNotFoundError:
            print(f"Error: File {filename} not found")
        return hashes
    
    def md5_hash(self, password: str) -> str:
        """Generate MD5 hash of a password"""
        return hashlib.md5(password.encode()).hexdigest()
    
    def generate_passwords(self, length: int):
        """Generate all possible passwords of given length"""
        for combination in itertools.product(self.charset, repeat=length):
            yield ''.join(combination)
    
    def crack_passwords(self, target_hashes: Set[str]) -> List[str]:
        """
        Crack passwords using brute force attack
        Returns list of cracked passwords
        """
        cracked = []
        total_attempts = 0
        
        print(f"Starting brute force attack...")
        print(f"Character set: {self.charset}")
        print(f"Password length range: {self.min_length}-{self.max_length}")
        print(f"Target hashes: {len(target_hashes)}")
        print("-" * 50)
        
        start_time = time.time()
        
        # Try passwords of each length from min to max
        for length in range(self.min_length, self.max_length + 1):
            print(f"Trying passwords of length {length}...")
            
            # Calculate total combinations for this length
            total_combinations = len(self.charset) ** length
            print(f"Total combinations to try: {total_combinations:,}")
            
            passwords_tried = 0
            
            # Generate and test each password
            for password in self.generate_passwords(length):
                passwords_tried += 1
                total_attempts += 1
                
                # Generate MD5 hash of current password
                hash_value = self.md5_hash(password)
                
                # Check if this hash matches any target hash
                if hash_value in target_hashes:
                    cracked.append(password)
                    target_hashes.remove(hash_value)  # Remove found hash to avoid duplicates
                    print(f"✓ CRACKED: '{password}' -> {hash_value}")
                    
                    # Update current progress for interrupt handling
                    self.current_cracked = cracked.copy()
                    
                    # Save progress immediately when a password is found
                    all_found = self.cracked_passwords + cracked
                    self.save_results(all_found, "cracked_passwords_progress.txt")
                
                # Progress indicator
                if passwords_tried % 100000 == 0:
                    elapsed = time.time() - start_time
                    rate = total_attempts / elapsed if elapsed > 0 else 0
                    print(f"  Progress: {passwords_tried:,}/{total_combinations:,} "
                          f"({passwords_tried/total_combinations*100:.1f}%) "
                          f"- Rate: {rate:.0f} passwords/sec "
                          f"- Found: {len(cracked)}")
                    
                    # Save progress every 100k attempts to avoid losing work
                    if cracked:
                        all_found = self.cracked_passwords + cracked
                        self.save_results(all_found, "cracked_passwords_progress.txt")
                
                # If we've found all hashes, we can stop early
                if not target_hashes:
                    print("All hashes cracked! Stopping early.")
                    break
            
            print(f"Completed length {length}: Found {len(cracked)} total passwords so far")
            
            # Save progress after each length completion
            if cracked:
                all_found = self.cracked_passwords + cracked
                self.save_results(all_found, "cracked_passwords_progress.txt")
            
            # If we've found all hashes, we can stop
            if not target_hashes:
                break
        
        elapsed_time = time.time() - start_time
        print("-" * 50)
        print(f"Brute force completed!")
        print(f"Total time: {elapsed_time:.2f} seconds")
        print(f"Total attempts: {total_attempts:,}")
        print(f"Passwords cracked: {len(cracked)}")
        if len(cracked) + len(target_hashes) > 0:
            print(f"Success rate: {len(cracked)/(len(cracked) + len(target_hashes))*100:.1f}%")
        
        return cracked
    
    def save_results(self, passwords: List[str], filename: str = "cracked_passwords.txt"):
        """Save cracked passwords to file"""
        try:
            with open(filename, 'w') as file:
                for password in passwords:
                    file.write(password + '\n')
            print(f"Results saved to {filename}")
        except Exception as e:
            print(f"Error saving results: {e}")
    
    def run_full_attack(self):
        """Run the complete password cracking attack on all three files"""
        hash_files = [
            "md5_30_passwords-pt1.txt",
            "md5_30_passwords-pt2.txt", 
            "md5_30_passwords-pt3.txt"
        ]
        
        all_hashes = set()
        
        # Load all hashes from all files
        for filename in hash_files:
            file_hashes = self.load_hashes(filename)
            all_hashes.update(file_hashes)
        
        print(f"\nTotal unique hashes to crack: {len(all_hashes)}")
        
        # Check if we have previous progress
        try:
            with open("cracked_passwords_progress.txt", 'r') as f:
                previous_passwords = [line.strip() for line in f if line.strip()]
            if previous_passwords:
                print(f"\nFound previous progress: {len(previous_passwords)} passwords already cracked")
                print("Continuing from where we left off...")
                
                # Remove already cracked hashes from target set
                for password in previous_passwords:
                    hash_value = self.md5_hash(password)
                    all_hashes.discard(hash_value)
                
                self.cracked_passwords = previous_passwords.copy()
                print(f"Remaining hashes to crack: {len(all_hashes)}")
        except FileNotFoundError:
            print("No previous progress found, starting fresh...")
        
        try:
            # Perform the attack
            cracked_passwords = self.crack_passwords(all_hashes)
            
            # Combine with any previous results
            all_cracked = self.cracked_passwords + cracked_passwords
            
            # Save final results
            self.save_results(all_cracked)
            
        except KeyboardInterrupt:
            print("\n\nAttack interrupted by user!")
            # Still save whatever we found
            all_cracked = self.cracked_passwords + (getattr(self, 'current_cracked', []))
            if all_cracked:
                self.save_results(all_cracked)
                print(f"Saved {len(all_cracked)} cracked passwords before exit.")
            return
        
        # Display summary
        print("\n" + "="*50)
        print("FINAL RESULTS")
        print("="*50)
        print(f"Total passwords cracked: {len(all_cracked)}")
        print(f"Target (60+ out of 90): {'PASS' if len(all_cracked) >= 60 else 'FAIL'}")
        
        if all_cracked:
            print("\nCracked passwords:")
            for i, password in enumerate(sorted(all_cracked), 1):
                print(f"{i:2d}. {password}")


def main():
    """Main function to run the password cracker"""
    print("="*50)
    print("HW2 Part 3: Password Cracker")
    print("MD5 Brute Force Attack")
    print("="*50)
    
    cracker = PasswordCracker()
    cracker.run_full_attack()


if __name__ == "__main__":
    main()