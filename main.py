import wave
from cryptography.fernet import Fernet

# Generate a key for encryption
key = Fernet.generate_key()
cipher = Fernet(key)


# Encrypting the message
print("\nEncoding Message...")

# Message to be encrypted
message = str(input("Enter your message: ")).encode()

encrypted_message = cipher.encrypt(message)

print("\nKey:", key.hex())
print("Encrypted message:", encrypted_message.hex())

audio = wave.open("sample.wav", mode="rb")
frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
string = encrypted_message

string = str(string)
string = string + int((len(frame_bytes) - (len(string) * 8 * 8)) / 8) * '#'
bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in string])))

for i, bit in enumerate(bits):
    frame_bytes[i] = (frame_bytes[i] & 254) | bit
frame_modified = bytes(frame_bytes)

# for i in range(0, 10):
#     print(frame_bytes[i])

newAudio = wave.open('output.wav', 'wb')
newAudio.setparams(audio.getparams())
newAudio.writeframes(frame_modified)
newAudio.close()
audio.close()
print("\nSuccessfully embedded message inside output.wav")

#Decrypting the message
print("\nDecoding Message...")
audio = wave.open("output.wav", mode='rb')
frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
string = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in range(0, len(extracted), 8))
decoded = string.split("###")[0]
decoded = decoded[slice(2, len(decoded)-1)].encode()

decrypted_message = cipher.decrypt(decoded)
print("Successfully decoded: " + decrypted_message.decode())
audio.close()