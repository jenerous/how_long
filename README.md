# status update on dd or other copy functions
Prints the time left based on given estimated final size of a file being copied.

## Usage
Example: You're using dd to clone an SD-card to your computer. You know the card is 64GB of size.
```
# carefully change input and output!
# dd if=/dev/sda of=sdbackup.img bs=2M
```

During this is running, you wonder how long it is going to take.
You can find out with this script:
```
./how_long.py sdbackup.img 64GB
```
You will get a status message every few seconds:
```
2.09GB (3.27%) 80.80MB/s -> 13min 4s to finish
```
The output is currently set to GBs for the overall size and MBs for the write speed. You can change this within the scripts easily.
You can give a third argument to the script to define the seconds to wait between reads.
