This folder contains the voice activity predictions in the CSV files:
  First column = Timestamp (sec.)
  Second column = Voice Act. (-1 to +1 , threshold at 0, -1 is unvoiced)

It also contains scripts to cut out the voiced segments from the segment wave files (*.sh).
The segment wave files must be placed in ../../Audio/wav/
and named according to the following example:
  237_2_Northwind_audio.wav
for 
  237_2_Northwind_audio.mp4

The wave files are not included in the distribution, but can easily be produced with
mplayer, for example, from the mp4 files:
  mplayer -ao pcm:file=../wav/<filename>.wav <filename>.mp4

