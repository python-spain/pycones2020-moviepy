#!/usr/bin/env python
""" Script para la creación de los vídeos de la PyconES 2020

  El Script necesita:
  1. Foto de inicio : foto_inicio.png que será la que se utilizará para crear el video inicial 5s
  2. Vídeo principal
  3. Vídeo final: por defecto video_end.mp4

  El resultado se guarda como nombre del vídeo principal

  Para simplificar supondremos que se sigue la convención:

  Foto inicio: video_principal.png
  Vídeo principal: video_principal.mp4
"""

from moviepy.editor import concatenate_videoclips
from moviepy.editor import VideoFileClip, ImageClip
import argparse

def convert(nombre):
    # Generamos la entradilla
    clip = ImageClip('{}.png'.format(nombre)).set_duration(5)
    clip.write_videofile('{}_start.mp4'.format(nombre), fps=24)
    clip.close()

    # Generamos vídeo final
    clip1 = VideoFileClip('{}_start.mp4'.format(nombre))
    clip2 = VideoFileClip('{}.mp4'.format(nombre))
    clip3 = VideoFileClip('video_end.mp4')

    final = concatenate_videoclips([clip1, clip2, clip3], method="compose")
    final.write_videofile('{}_final.mp4'.format(nombre))
    final.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--video', help='nombre del video principal sin mp4')
    args = parser.parse_args()
    if args.video:
        convert(args.video)
    else:
        print (__doc__)

