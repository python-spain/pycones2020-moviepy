#!/usr/bin/env python
""" Script para la creación de los vídeos de la PyconES 2020

  El Script necesita que:
      1. todos los vídeos estén en la carpeta 'videos'
      2. Todas las imágenes estén en la carpeta 'Slides_start_end'
  El script está en la carpeta base:
      /create.py
      |--videos/
      |--Slides_start_end/
          
  Se ejecuta así:
     > python create.py --name barcelona --outname Barcelona
  Busca todo lo que lleve 'barcelona' en el nombre y lo usa para crear el vídeo
  final que se llamará 'Barcelona_final.mp4'
"""

import argparse
from pathlib import Path

from PIL import Image
import numpy as np
from moviepy.editor import concatenate_videoclips
from moviepy.editor import VideoFileClip, ImageClip


video_formats = (".mp4", ".mov", ".ogg", ".webm")

def convert(name, outname):
    # Buscamos el vídeo en la carpeta
    p = Path("videos")
    files = list(p.glob("*"))
    for f in files:
        fstr = str(f).lower()
        if f.is_file() and f.suffix.lower() in video_formats and name in fstr:
            video_path = str(f)
            break
    print(video_path)
    
    # Buscamos la carátula
    p = Path("Slides_start_end")
    files = list(p.glob("*"))
    for f in files:
        fstr = str(f).lower()
        if (
            f.is_file() and 
            "1440" in str(f) and 
            "end_1440" not in str(f) and
            name in fstr
            ):
            cover_path = str(f)
            break
    print(cover_path)
    
    # Buscamos la imagen de cierre
    p = Path("Slides_start_end", "end_1440.png")
    end_path = str(p)
    print(end_path)
    
    # Buscamos el ancho y alto del vídeo
    clip = VideoFileClip(video_path)
    clip_part = clip.subclip(0, 5)
    clip_size = clip_part.size
    
    # Ponemos el cover y final al mismo tamaño que el vídeo
    im = Image.open(cover_path)
    out = im.resize(clip_size)
    arr_in = np.array(out)
    
    im = Image.open(end_path)
    out = im.resize(clip_size)
    arr_out = np.array(out)
        
    # Generamos la entradilla
    clip = ImageClip(arr_in).set_duration(5)
    clip.write_videofile('video_start.mp4', fps=24)
    clip.close()
    
    # Generamos el cierre
    clip = ImageClip(arr_out).set_duration(5)
    clip.write_videofile('video_end.mp4', fps=24)
    clip.close()

    # Generamos vídeo final
    clip1 = VideoFileClip('video_start.mp4')
    clip2 = VideoFileClip(video_path)
    clip3 = VideoFileClip('video_end.mp4')

    final = concatenate_videoclips([clip1, clip2, clip3], method="compose")
    final.write_videofile(f'{outname}_final.mp4')
    final.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--name', help='nombre a buscar')
    parser.add_argument('--outname', help='nombre del vídeo final')
    args = parser.parse_args()
    if args.name and args.outname:
        convert(args.name, args.outname)
    else:
        print (__doc__)