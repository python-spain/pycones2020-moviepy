#!/usr/bin/env python
"""  @@@ CASO ESPECIAL PARA CyL @@@
  Script para la creación de los vídeos de la PyconES 2020

  El Script necesita que:
      1. todos los vídeos estén en la carpeta 'videos'
      2. Todas las imágenes estén en la carpeta 'Slides_start_end'
  El script está en la carpeta base:
      /create.py
      |--videos/
      |--Slides_start_end/
          
  Se ejecuta así:
     > python create_communities_PyDocsEs.py --outname PythonDocEs
  Crea el vídeo final que se llamará 'PythonDocEs_final.mp4'
"""

import argparse
from pathlib import Path

from PIL import Image
import numpy as np
from moviepy.editor import concatenate_videoclips
from moviepy.editor import VideoFileClip, ImageClip


video_formats = (".mp4", ".mov", ".ogg", ".webm")

def convert(outname):
    
    # Buscamos el vídeo de Python Doc Es en la carpeta
    # El vídeo original de Python Docs Es estaba en vertical. Lo he tenido que 
    # transformar y lo he guardado en horizontal (y en mp4) usando:
    # ffmpeg -i videos/proyecto\ python-docs-es.mp4 -vf 'split[original][copy];[copy]scale=ih*16/9:-1,crop=h=iw*9/16,gblur=sigma=20[blurred];[blurred][original]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2' videos/proyecto\ python-docs-es_reformat.mp4
    # Ver https://www.junian.net/tech/ffmpeg-vertical-video-blur/
    p = Path("videos", "proyecto python-docs-es_reformat.mp4")
    video_path = str(p)
    print(video_path)
    
    # Buscamos la carátula
    p = Path("Slides_start_end", "python_doc_es_1440.png")
    cover_path = str(p)
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

    final = concatenate_videoclips([clip1, clip2, clip3], 
        method="compose"
    )
    final.write_videofile(f'{outname}_final.mp4')
    final.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--outname', help='nombre del vídeo final')
    args = parser.parse_args()
    if args.outname:
        convert(args.outname)
    else:
        print (__doc__)