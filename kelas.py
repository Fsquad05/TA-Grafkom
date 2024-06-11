from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import numpy as np

# Inisialisasi aplikasi
app = Ursina()

orang_bergerak = Entity(model = 'img/rp_dennis_posed_004_100k.OBJ', texture='rp_dennis_posed_004_dif.jpg', scale=(0.015), position=(3.5, 0, -3.5), double_sided=True, rotation = (0,-90,0))
orang_bergerak.collider = 'box'

def dda_line(x0, y0, z0, x1, y1, z1):
    points = []
    dx = x1 - x0
    dy = y1 - y0
    dz = z1 - z0
    steps = int(max(abs(dx), abs(dy), abs(dz)))
    
    x_inc = dx / steps
    y_inc = dy / steps
    z_inc = dz / steps

    x = x0
    y = y0
    z = z0
    for i in range(steps + 1):
        points.append((x, y, z))
        x += x_inc
        y += y_inc
        z += z_inc

    return points

# Fungsi animasi untuk menggerakkan sesuai rute yang diinginkan
def pergerakan():
    # Tahap 1: Bergerak ke sumbu X sejauh 5 unit
    start_pos   = Vec3(20, 0, -20.5)
    mid_pos     = Vec3(11, 0, -20.5)
    end_pos     = Vec3(11, 0, -3.95)
    endless_pos = Vec3(20, 0, -3.95)
    
    points1     = dda_line(start_pos.x, start_pos.y, start_pos.z, mid_pos.x, mid_pos.y, mid_pos.z)
    points2     = dda_line(mid_pos.x, mid_pos.y, mid_pos.z, end_pos.x, end_pos.y, end_pos.z)
    points3     = dda_line(end_pos.x, end_pos.y, end_pos.z, endless_pos.x, endless_pos.y, endless_pos.z)
    duration1   = 2  
    duration2   = 4  
    duration3   = 6  
    
    # Tampilkan titik-titik 
    for point in points1 + points2 + points3:
        Entity(model='sphere', scale=0.2, color=color.red, position=(point[0], point[1], point[2]))
    
    # Animasi bergerak ke titik-titik yang dihitung oleh algoritma DDA
    for i, point in enumerate(points1):
        invoke(
            orang_bergerak.animate_position,
            Vec3(point[0], point[1], point[2]),
            duration=duration1 / len(points1),
            delay=i * (duration1 / len(points1)),
            curve=curve.linear
        )
    
    # Animasi bergerak ke titik-titik yang dihitung oleh algoritma DDA untuk tahap 2
    for i, point in enumerate(points2):
        invoke(
            orang_bergerak.animate_position,
            Vec3(point[0], point[1], point[2]),
            duration=duration2 / len(points2),
            delay=duration1 + i * (duration2 / len(points2)),
            curve=curve.linear
        )
    
    # Animasi bergerak ke titik-titik yang dihitung oleh algoritma DDA untuk tahap 2
    for i, point in enumerate(points3):
        invoke(
            orang_bergerak.animate_position,
            Vec3(point[0], point[1], point[2]),
            duration=duration3 / len(points3),
            delay=duration3 + i * (duration3 / len(points3)),
            curve=curve.linear
        )
    
    # Kembali ke posisi awal setelah mencapai akhir
    invoke(pergerakan, delay=duration1 + duration2 + duration3 + 1)

# Mulai animasi
pergerakan()

# Membuat kelas dengan objek-objek di dalamnya
class RuangKelas(Entity):
    def __init__(self):
        super().__init__()

#         marker_scale    = (0.2, 0.2, 0.2)
#         marker_color_p  = color.red
#         marker_color_n  = color.blue

# # Sudut x
#         x_marker_positive = Entity(model='cube', scale=marker_scale, color=marker_color_p)
#         x_marker_negative = Entity(model='cube', scale=marker_scale, color=marker_color_n)
#         x_marker_positive.position = (0.5, 2, 0)
#         x_marker_negative.position = (-0.5, 2, 0)

# # Sudut y
#         y_marker_positive = Entity(model='icosphere', scale=marker_scale, color=marker_color_p)
#         y_marker_negative = Entity(model='icosphere', scale=marker_scale, color=marker_color_n)
#         y_marker_positive.position = (0, 2.5, 0)
#         y_marker_negative.position = (0, 1.5, 0)

# # Sudut z
#         z_marker_positive = Entity(model='sphere', scale=marker_scale, color=marker_color_p)
#         z_marker_negative = Entity(model='sphere', scale=marker_scale, color=marker_color_n)
#         z_marker_positive.position = (0, 2, 0.5)
#         z_marker_negative.position = (0, 2, -0.5)

        kayu = load_texture('color.png')

        # Lantai dan Atap
        self.lantai = Entity(model ='plane', texture = 'img/lantai.jpg', scale = (50, 1, 50), texture_scale=(10, 20), collider = 'box')
        self.atap   = Entity(model ='cube', scale=(50, 0.1, 60), position=(0, 5, 3.5), color=color.gray, collider='box')

        # lampu & speaker
        self.lampu          = Entity(model ='cube', texture = 'white_cube', scale=(0.7, 0.1, 2), color=(1, 0.98, 1, 1), position=(3, 4.98, 1.5), collider='box')
        self.speaker        = Entity(model ='sphere', scale=(0.7, 0.1, 0.7), color=(1, 0.98, 1, 1), position=(0, 4.98, 1), collider='box')
        self.lampu_kanan    = duplicate(self.lampu, x=-3)
        self.lampu_kananB   = duplicate(self.lampu, z=8)
        self.lampu_kiriB    = duplicate(self.lampu, x=-3, z=8)
        self.speakerB       = duplicate(self.speaker, z=9)
        self.speaker_luar   = duplicate(self.speaker, x=11, z=9)
        self.speaker_luar   = duplicate(self.speaker, x=11, z=-1)
        self.speaker_luar   = duplicate(self.speaker, x=11, z=-9)
        self.speaker_luar   = duplicate(self.speaker, x=11, z=-21)
        self.speaker_luar   = duplicate(self.speaker, x=17, z=-9)

        # Dinding Ruang 1
        self.depan          = Entity(model = 'cube', scale = (15, 5, 0.1), position = (0, 2.5, -5), color=(0.89, 0.89, 0.89, 1), collider = 'box')
        self.kanan          = Entity(model = 'cube', scale = (0.1, 5, 17), position = (-7.4, 2.5, 3.5), color=(0.89, 0.89, 0.89, 1), collider = 'box')
        self.kiri           = Entity(model = 'cube', scale = (0.1, 5, 15), position=(7.45, 2.5, 4.5), color=(0.89, 0.89, 0.89, 1), collider = 'box')
        self.kiri_atas      = Entity(model = 'cube', scale=(0.1, 2, 2), position=(7.45, 4, -3.95), color=(0.89, 0.89, 0.89, 1), collider='box')
        self.belakang_bawah = Entity(model = 'cube', scale=(14.8, 1.5, 0.1), position=(0,0.8, 12), color=(0.89, 0.89, 0.89, 1), collider='box')  
        self.belakang_atas  = Entity(model = 'cube', scale=(14.8, 1, 0.1), position=(0, 4.5, 12), color=(0.89, 0.89, 0.89, 1), collider='box')  
        self.belakang_kiri  = Entity(model = 'cube', scale=(2.5, 2.5, 0.1), position=(-6.2, 2.8, 12), color=(0.89, 0.89, 0.89, 1), collider='box') 
        self.belakang_kanan = Entity(model = 'cube', scale=(2.5, 2.5, 0.1), position=(6.2, 2.8, 12), color=(0.89, 0.89, 0.89, 1), collider='box') 
        self.latar          = Entity(model = 'cube', texture='pemandangan.jpg', scale=(10, 3, 0.1), position=(0,2.8, 12.1), collider='box')  
        self.sign_kelas     = Entity(model = 'cube', texture='img/R502.png', scale=(0.1, 0.5, 1.5), position=(7.455, 3.6, -3.95), collider='box', rotation = (0,0,0))

        # gypsum ruang 1
        self.gypsum_depanB    = Entity(model = 'cube', scale = (15, 0.1, 0.1), position = (0, 0.1, -4.95), texture = 'img/lantai.jpg', color=(0.89, 0.89, 0.89, 1), collider = 'box')
        self.gypsum_depanA    = Entity(model = 'cube', scale = (15, 0.1, 0.1), position = (0, 4.9, -4.95), texture = 'white_cube', color=(0.89, 0.89, 0.89, 1), collider = 'box')
        self.gypsum_kananB    = Entity(model = 'cube', scale = (0.1, 0.1, 17), position = (-7.35, 0.1, 3.5), texture = 'img/lantai.jpg', color=(0.89, 0.89, 0.89, 1), collider = 'box')
        self.gypsum_kananA    = Entity(model = 'cube', scale = (0.1, 0.1, 17), position = (-7.35, 4.9, 3.5), texture = 'white_cube', color=(0.89, 0.89, 0.89, 1), collider = 'box')
        self.gypsum_belakangB = duplicate(self.gypsum_depanB,z=11.95)
        self.gypsum_belakangA = duplicate(self.gypsum_depanA,z=11.95)
        self.gypsum_kiriB     = duplicate(self.gypsum_kananB,scale_z=15, x=7.35,z=4.5)
        self.gypsum_kiriA     = duplicate(self.gypsum_kananA,scale_z=17, x=7.35,z=3.5)
        self.gypsum_luarB     = duplicate(self.gypsum_kananB,scale_z=15, x=7.55,z=4.5)
        self.gypsum_luarA     = duplicate(self.gypsum_kananA,scale_z=35, x=7.55,z=-5)
        
        # gypsum ruang 2
        self.gypsum_depanA  = duplicate(self.gypsum_depanA,x=21.96,z=-5.2)
        self.gypsum_depanB  = duplicate(self.gypsum_depanB,x=21.96,y=0.1, z=-5.2)
        self.gypsum_luarB   = duplicate(self.gypsum_kananB,scale_z=15, x=14.45,z=4.5)
        self.gypsum_luarA   = duplicate(self.gypsum_kananA,scale_z=17.3, x=14.45,z=3.4)
        
        # gypsum ruang 3
        self.gypsum_belakangA   = duplicate(self.gypsum_depanA,x=21.96,z=-12.9)
        self.gypsum_luarA       = duplicate(self.gypsum_kananA,scale_z=15.3, x=14.45,z=-20.5)
        self.gypsum_luarB       = duplicate(self.gypsum_kananB,scale_z=15.3, x=14.46, y=0.1, z=-20.5)
        self.gypsum_belakangB   = duplicate(self.gypsum_depanB,x=21.96, y=0.1, z=-12.9)

        # gypsum ruang 4
        self.gypsum_luarB = duplicate(self.gypsum_kananB,scale_z=15, x=7.55,z=-12.55)

        # kusen ruang 1
        self.kkanan = Entity(model = 'cube', scale = (0.35, 3, 0.2), position=(7.45, 1.5, -2.95), color=(0.89, 0.89, 1, 1), collider = 'box')
        self.kkiri  = Entity(model = 'cube', scale = (0.35, 3.3, 0.2), position=(7.45, 1.5, -5), color=(0.89, 0.89, 1, 1), collider = 'box')
        self.katas  = Entity(model = 'cube', scale=(0.35, 0.2, 2.2), position=(7.45, 3.05, -3.95), color=(0.89, 0.89, 1, 1), collider='box')

        # kusen ruang 2
        self.kkanan = Entity(model = 'cube', scale = (0.35, 3, 0.2), position=(14.45, 1.5, -2.95), color=(0.89, 0.89, 1, 1), collider = 'box')
        self.kkiri  = Entity(model = 'cube', scale = (0.35, 3.3, 0.2), position=(14.45, 1.5, -5), color=(0.89, 0.89, 1, 1), collider = 'box')
        self.katas  = Entity(model = 'cube', scale=(0.35, 0.2, 2.2), position=(14.45, 3.05, -3.95), color=(0.89, 0.89, 1, 1), collider='box')
        
        # kusen ruang 3
        self.kkanan = Entity(model = 'cube', scale = (0.35, 3, 0.2), position=(14.45, 1.5, -19.5), color=(0.89, 0.89, 1, 1), collider = 'box')
        self.kkiri  = Entity(model = 'cube', scale = (0.35, 3.3, 0.2), position=(14.45, 1.5, -21.55), color=(0.89, 0.89, 1, 1), collider = 'box')
        self.katas  = Entity(model = 'cube', scale=(0.35, 0.2, 2.2), position=(14.45, 3.05, -20.5), color=(0.89, 0.89, 1, 1), collider='box')
        
        # kusen ruang 4
        self.kkanan = Entity(model = 'cube', scale = (0.35, 3, 0.2), position=(7.45, 1.5, -22), color=(0.89, 0.89, 1, 1), collider = 'box')
        self.kkiri  = Entity(model = 'cube', scale = (0.35, 3.3, 0.2), position=(7.45, 1.5, -20), color=(0.89, 0.89, 1, 1), collider = 'box')
        self.katas  = Entity(model = 'cube', scale=(0.35, 0.2, 2.2), position=(7.45, 3.05, -21), color=(0.89, 0.89, 1, 1), collider='box')

        # jendela atas ujung
        self.atas_bawah     = Entity(model='cube', scale=(0.14, 0.1, 2.55), position=(7.45, 3.3, 9), color=(0.89, 0.89, 1, 1), collider='box')
        self.atas_atas      = Entity(model='cube', scale=(0.14, 0.1, 2.55), position=(7.45, 4.55, 9), color=(0.89, 0.89, 1, 1), collider='box')
        self.atas_kanan     = Entity(model='cube', scale=(0.14, 1.33, 0.1), position=(7.45, 3.93, 7.75), color=(0.89, 0.89, 1, 1), collider='box')
        self.atas_tengah    = Entity(model='cube', scale=(0.14, 1.33, 0.1), position=(7.45, 3.93, 9), color=(0.89, 0.89, 1, 1), collider='box')
        self.atas_kiri      = Entity(model='cube', scale=(0.14, 1.33, 0.1), position=(7.45, 3.93, 10.25), color=(0.89, 0.89, 1, 1), collider='box')
        self.jendela_atas   = Entity(model='cube', texture='kaca_atas1.jpg', scale=(0.12, 1.2, 2.5), position=(7.45, 3.9, 9), collider='box')

        # jendela atas deket pintu
        self.atas_bawah     = Entity(model='cube', scale=(0.14, 0.1, 2.55), position=(7.45, 3.3, 2.7), color=(0.89, 0.89, 1, 1), collider='box')
        self.atas_atas      = Entity(model='cube', scale=(0.14, 0.1, 2.55), position=(7.45, 4.55, 2.7), color=(0.89, 0.89, 1, 1), collider='box')
        self.atas_kanan     = Entity(model='cube', scale=(0.14, 1.33, 0.1), position=(7.45, 3.93, 1.45), color=(0.89, 0.89, 1, 1), collider='box')
        self.atas_tengah    = Entity(model='cube', scale=(0.14, 1.33, 0.1), position=(7.45, 3.93, 2.7), color=(0.89, 0.89, 1, 1), collider='box')
        self.atas_kiri      = Entity(model='cube', scale=(0.14, 1.33, 0.1), position=(7.45, 3.93, 3.95), color=(0.89, 0.89, 1, 1), collider='box')
        self.jendela_atas   = Entity(model='cube', texture='kaca_atas1.jpg', scale=(0.12, 1.2, 2.5), position=(7.45, 3.9, 2.7), collider='box')
        
        # jendela atas ruang 4 deket pintu
        self.atas_bawah     = Entity(model='cube', scale=(0.14, 0.1, 2.55), position=(7.45, 3.3, -17), color=(0.89, 0.89, 1, 1), collider='box')
        self.atas_atas      = Entity(model='cube', scale=(0.14, 0.1, 2.55), position=(7.45, 4.55, -17), color=(0.89, 0.89, 1, 1), collider='box')
        self.atas_kanan     = Entity(model='cube', scale=(0.14, 1.33, 0.1), position=(7.45, 3.93, -15.75), color=(0.89, 0.89, 1, 1), collider='box')
        self.atas_tengah    = Entity(model='cube', scale=(0.14, 1.33, 0.1), position=(7.45, 3.93, -17), color=(0.89, 0.89, 1, 1), collider='box')
        self.atas_kiri      = Entity(model='cube', scale=(0.14, 1.33, 0.1), position=(7.45, 3.93, -18.25), color=(0.89, 0.89, 1, 1), collider='box')
        self.jendela_atas   = Entity(model='cube', texture='kaca_atas1.jpg', scale=(0.12, 1.2, 2.5), position=(7.45, 3.9, -17), collider='box')
        
        # jendela atas ruang 4 
        self.atas_bawah     = Entity(model='cube', scale=(0.14, 0.1, 2.55), position=(7.45, 3.3, -12), color=(0.89, 0.89, 1, 1), collider='box')
        self.atas_atas      = Entity(model='cube', scale=(0.14, 0.1, 2.55), position=(7.45, 4.55, -12), color=(0.89, 0.89, 1, 1), collider='box')
        self.atas_kanan     = Entity(model='cube', scale=(0.14, 1.33, 0.1), position=(7.45, 3.93, -10.75), color=(0.89, 0.89, 1, 1), collider='box')
        self.atas_tengah    = Entity(model='cube', scale=(0.14, 1.33, 0.1), position=(7.45, 3.93, -12), color=(0.89, 0.89, 1, 1), collider='box')
        self.atas_kiri      = Entity(model='cube', scale=(0.14, 1.33, 0.1), position=(7.45, 3.93, -13.25), color=(0.89, 0.89, 1, 1), collider='box')
        self.jendela_atas   = Entity(model='cube', texture='kaca_atas1.jpg', scale=(0.12, 1.2, 2.5), position=(7.45, 3.9, -12), collider='box')
       
        # jendela atas ruang 2 belakang
        self.atas_bawah     = Entity(model='cube', scale=(0.14, 0.1, 2.55), position=(14.45, 3.3, 9), color=(0.89, 0.89, 1, 1), collider='box')
        self.atas_atas      = Entity(model='cube', scale=(0.14, 0.1, 2.55), position=(14.45, 4.55, 9), color=(0.89, 0.89, 1, 1), collider='box')
        self.atas_kanan     = Entity(model='cube', scale=(0.14, 1.33, 0.1), position=(14.45, 3.93, 7.75), color=(0.89, 0.89, 1, 1), collider='box')
        self.atas_tengah    = Entity(model='cube', scale=(0.14, 1.33, 0.1), position=(14.45, 3.93, 9), color=(0.89, 0.89, 1, 1), collider='box')
        self.atas_kiri      = Entity(model='cube', scale=(0.14, 1.33, 0.1), position=(14.45, 3.93, 10.25), color=(0.89, 0.89, 1, 1), collider='box')
        self.jendela_atas   = Entity(model='cube', texture='kaca_atas1.jpg', scale=(0.12, 1.2, 2.5), position=(14.45, 3.9, 9), collider='box')

        # jendela atas ruang 2 depan
        self.atas_bawah     = Entity(model='cube', scale=(0.14, 0.1, 2.55), position=(14.45, 3.3, 1), color=(0.89, 0.89, 1, 1), collider='box')
        self.atas_atas      = Entity(model='cube', scale=(0.14, 0.1, 2.55), position=(14.45, 4.55, 1), color=(0.89, 0.89, 1, 1), collider='box')
        self.atas_kanan     = Entity(model='cube', scale=(0.14, 1.33, 0.1), position=(14.45, 3.93, -0.25), color=(0.89, 0.89, 1, 1), collider='box')
        self.atas_tengah    = Entity(model='cube', scale=(0.14, 1.33, 0.1), position=(14.45, 3.93, 1), color=(0.89, 0.89, 1, 1), collider='box')
        self.atas_kiri      = Entity(model='cube', scale=(0.14, 1.33, 0.1), position=(14.45, 3.93, 2.25), color=(0.89, 0.89, 1, 1), collider='box')
        self.jendela_atas   = Entity(model='cube', texture='kaca_atas1.jpg', scale=(0.12, 1.2, 2.5), position=(14.45, 3.9, 1), collider='box')

        # dinding ruang 2
        self.kiri       = Entity(model = 'cube', scale = (0.1, 5, 15), position=(14.5, 2.5, 4.5), color=(0.89, 0.89, 0.89, 1), collider = 'box')
        self.kiri_atas  = Entity(model = 'cube', scale=(0.1, 2, 2), position=(14.5, 4, -3.95), color=(0.89, 0.89, 0.89, 1), collider='box')
        self.pintu1     = Entity(model = 'cube', texture='img/bg_pintu.jpg', scale=(0.1, 3, 2), position=(14.5, 1.5, -3.95), collider='box', rotation = (0,180,0))
        self.depan      = Entity(model = 'cube', scale = (15, 5, 0.3), position = (21.96, 2.5, -5), color=(0.89, 0.89, 0.89, 1), collider = 'box')
        self.sign_kelas = Entity(model = 'cube', texture='img/R501.png', scale=(0.1, 0.5, 1.5), position=(14.49, 3.6, -3.95), collider='box', rotation = (0,180,0))
        
        # dinding ruang 3
        self.belakang   = Entity(model = 'cube', scale = (15, 5, 0.1), position = (22, 2.5, -13), color=(0.89, 0.89, 0.89, 1), collider = 'box')
        self.kiri       = Entity(model = 'cube', scale = (0.1, 5, 15), position=(14.5, 2.5, -20.5), color=(0.89, 0.89, 0.89, 1), collider = 'box')
        self.pintu2     = Entity(model = 'cube', texture='img/pintu_wc1.jpg', scale=(0.1, 3, 2), position=(14.45, 1.5, -20.5), collider='box', rotation = (0,180,0))
        self.sign_wc    = Entity(model = 'cube', texture='img/sign wc.png', scale=(0.1, 0.5, 1.5), position=(14.45, 3.6, -20.5), collider='box', rotation = (0,180,0))
        
        # dinding ruang 4
        self.kanan          = Entity(model = 'cube', scale = (0.1, 5, 15), position=(7.45, 2.5, -12.55), color=(0.89, 0.89, 0.89, 1), collider = 'box')
        self.kanan_atas     = Entity(model = 'cube', scale=(0.1, 2, 2), position=(7.45, 4, -21.05), color=(0.89, 0.89, 0.89, 1), collider='box')
        self.depan          = Entity(model = 'cube', scale = (15, 5, 0.1), position = (0, 2.5, -22.09), color=(0.89, 0.89, 0.89, 1), collider = 'box')
        self.pintu3         = Entity(model = 'cube', texture='img/bg_pintu.jpg', scale=(0.1, 3, 2), position=(7.45, 1.5, -21.05), collider='box', rotation = (0,180,0))
        self.kanan_depan    = Entity(model = 'cube', scale=(0.1, 5, 3.83), position=(7.45, 2.5, -24.05), color=(0.89, 0.89, 0.89, 1), collider='box')
        self.gypsum_luarB   = Entity(model = 'cube', scale=(0.1, 0.1, 3.83), texture = 'img/lantai.jpg', position=(7.55, 0.1, -24.05), color=(0.89, 0.89, 0.89, 1), collider='box')
        self.gypsum_luarA   = Entity(model = 'cube', scale=(0.1, 0.1, 3.83), texture = 'white_cube', position=(7.55, 4.9, -24.05), color=(0.89, 0.89, 0.89, 1), collider='box')
        self.sign_kelas     = Entity(model = 'cube', texture='img/R503.png', scale=(0.1, 0.5, 1.5), position=(7.47, 3.6, -21.05), collider='box', rotation = (0,0,0))
        
        #jeruji
        self.tembok_bawah   = Entity(model = 'cube', scale=(7, 1.6, 0.1), position=(11, 0.9, 12), color=(0.89, 0.89, 0.89, 1), collider='box') 
        self.tembok_atas    = Entity(model = 'cube', scale=(7, 1, 0.1), position=(11, 4.5, 12), color=(0.89, 0.89, 0.89, 1), collider='box') 
        self.besi_atas      = Entity(model = 'cube', scale=(7, 0.1, 0.1), position=(11, 3.95, 12), color=color.brown, collider='box') 
        self.besi_tengah    = Entity(model = 'cube', scale=(0.1, 2.3, 0.1), position=(7.55, 2.85, 12), color=color.brown, collider='box') 
        self.besi_tengah    = Entity(model = 'cube', scale=(0.1, 2.3, 0.1), position=(14.4, 2.85, 12), color=color.brown, collider='box') 
        self.besi_tengah    = duplicate(self.besi_tengah,x=8)
        self.besi_tengah    = duplicate(self.besi_tengah,x=8.45)
        self.besi_tengah    = duplicate(self.besi_tengah,x=8.9)
        self.besi_tengah    = duplicate(self.besi_tengah,x=9.35)
        self.besi_tengah    = duplicate(self.besi_tengah,x=9.8)
        self.besi_tengah    = duplicate(self.besi_tengah,x=10.25)
        self.besi_tengah1   = duplicate(self.besi_tengah,x=10.85, scale_x=0.2)
        self.besi_tengah2   = duplicate(self.besi_tengah,x=11, scale_x=0.2)
        self.besi_tengah    = duplicate(self.besi_tengah,x=11.6)
        self.besi_tengah    = duplicate(self.besi_tengah,x=12.05)
        self.besi_tengah    = duplicate(self.besi_tengah,x=12.5)
        self.besi_tengah    = duplicate(self.besi_tengah,x=12.95)
        self.besi_tengah    = duplicate(self.besi_tengah,x=13.4)
        self.besi_tengah    = duplicate(self.besi_tengah,x=13.85)
        self.besi_bawah     = Entity(model = 'cube', scale=(7, 0.1, 0.1), position=(11, 1.75, 12), color=color.brown, collider='box') 
        self.latar          = Entity(model = 'cube',texture='pemandangan.jpg', scale=(7, 3, 0.1), position=(10.9, 2.85, 12.1), collider='box')  
        self.gypsum_luarB   = Entity(model = 'cube', scale=(7, 0.1, 0.1), texture = 'img/lantai.jpg', position=(11, 0.1, 11.95), color=(0.89, 0.89, 0.89, 1), collider='box') 
        self.gypsum_luarA   = Entity(model = 'cube', scale=(7, 0.1, 0.1), texture = 'white_cube', position=(11, 4.9, 11.95), color=(0.89, 0.89, 0.89, 1), collider='box') 

        # dinding dan gypsum tembok luar
        self.tembok_bawah       = Entity(model = 'cube', scale=(7, 5, 0.1), position=(11, 2.5,-25), color=(0.89, 0.89, 0.89, 1), collider='box') 
        self.gypsum_luarB       = Entity(model = 'cube', scale=(7, 0.1, 0.1), texture = 'img/lantai.jpg', position=(11, 0.1,-24.9), color=(0.89, 0.89, 0.89, 1), collider='box') 
        self.gypsum_luarA       = Entity(model = 'cube', scale=(7, 0.1, 0.1), texture = 'white_cube', position=(11, 4.9,-24.9), color=(0.89, 0.89, 0.89, 1), collider='box') 
        self.tembok_penghalang  = Entity(model = 'cube', scale=(0.1, 5, 8), position=(19, 2.5,-9), color=(0.89, 0.89, 0.89, 1), collider='box') 
        self.gypsum_penghalangA = Entity(model = 'cube', texture = 'white_cube', scale=(0.1, 0.1, 8), position=(18.9, 4.9,-9), color=(0.89, 0.89, 0.89, 1), collider='box') 
        self.gypsum_penghalangB = Entity(model = 'cube', texture = 'img/lantai.jpg', scale=(0.1, 0.1, 8), position=(18.9, 0.1,-9), color=(0.89, 0.89, 0.89, 1), collider='box') 
        
        # Kerangka Jendela ruang 1
        self.kanan_ujung    = Entity(model = 'cube', scale=(0.1, 2.4, 0.1), position=(4.9, 2.8, 12), color=color.black, collider='box')  
        self.kanan_deket    = Entity(model = 'cube', scale=(0.1, 2.4, 0.1), position=(2, 2.8, 12), color=color.black, collider='box')  
        self.kiri_ujung     = Entity(model = 'cube', scale=(0.1, 2.4, 0.1), position=(-4.9, 2.8, 12), color=color.black, collider='box')  
        self.kiri_deket     = Entity(model = 'cube', scale=(0.1, 2.4, 0.1), position=(-2, 2.8, 12), color=color.black, collider='box')  
        self.kerangka_atas  = Entity(model = 'cube', scale=(9.9, 0.1, 0.1), position=(0, 1.6, 12), color=color.black, collider='box')  
        self.Kerangka_bawah = Entity(model = 'cube', scale=(9.9, 0.1, 0.1), position=(0, 3.95, 12), color=color.black, collider='box')  
        
        # Pembuangan AC
        self.aircooler1 = Entity(model = 'img/ac_split_A.obj', texture='ac_split_4k_BaseColor.png', scale=(0.02), position=(-6, 0.5, 12), double_sided=True, rotation = (0,0,0))  
        self.aircooler2 = Entity(model = 'img/ac_split_A.obj', texture='ac_split_4k_BaseColor.png', scale=(0.02), position=(6, 0.5, 12), double_sided=True, rotation = (0,0,0))  
        
        # korden
        self.korden_tengah  = Entity(model = 'img/curtain8.FBX', texture='Curtain_2_LP_Curtain_1_BaseColor.png', scale=(0.0015), position=(0, 0.5, 11.8), double_sided=True, rotation = (0,90,0))  
        self.korden_kiri    = Entity(model = 'img/curtain8.FBX', texture='Curtain_2_LP_Curtain_1_BaseColor.png', scale=(0.0015), position=(-4, 0.5, 11.8), double_sided=True, rotation = (0,90,0))  
        self.korden_kanan   = Entity(model = 'img/curtain8.FBX', texture='Curtain_2_LP_Curtain_1_BaseColor.png', scale=(0.0015), position=(4, 0.5, 11.8), double_sided=True, rotation = (0,90,0))  
        

        # Papan Tulis
        self.layar      = Entity(model = 'cube', texture='img/ppt.mp4', scale=(3, 2.2, 0.1), position=(1.75, 2.5, -4.88), collider='box', rotation_y=180)
        self.board      = Entity(model = 'cube', scale=(5.55, 3.3, 0.1), position=(2.78, 2.5, -4.95), color=(0.84, 0.84, 0.87, 1), collider='box')
        self.boarda     = Entity(model = 'cube', scale=(5.2, 3, 0.1), position=(2.78, 2.5, -4.9), color=color.white, collider='box')
        self.board1     = Entity(model = 'cube', scale=(5.55, 3.3, 0.1), position=(-2.78, 2.5, -4.95), color=(0.84, 0.84, 0.87, 1), collider='box')
        self.board1a    = Entity(model = 'cube', scale=(5.2, 3, 0.1), position=(-2.78, 2.5, -4.9), color=color.white, collider='box')
        self.pintu      = Entity(model = 'cube', texture='img/bg_pintu.jpg', scale=(2, 3, 0.1), position=(6.5, 1.5, -4.9), collider='box' )

        # AC
        self.ac_kanan   = Entity(model = 'Conditioner.obj', scale=(0.030), position=(7.1, 4, 0), texture='Conditioner_1K_BaseColor.tga', collider='box')
        self.dup        = duplicate(self.ac_kanan,x=-7,rotation_y=-180)
        
        # Tiang ruang 1
        self.tiangkanan = Entity(model = 'cube', scale=(1.5, 5, 1.5), position=(6.6, 2.5, 5), color=(0.89, 0.89, 0.89, 1), collider='box')
        self.tiangbawah = Entity(model = 'cube', texture = 'img/lantai.jpg', scale=(1.7, 0.1, 1.7), color=(0.89, 0.89, 0.89, 1), position=(6.6, 0.1, 5), collider='box')
        self.tiangatas  = Entity(model = 'cube', texture = 'white_cube', scale=(1.7, 0.1, 1.7), color=(0.89, 0.89, 0.89, 1), position=(6.6, 4.9, 5), collider='box')
        self.tiangkiri1  = duplicate(self.tiangbawah,x=-6.6)
        self.tiangbawah1 = duplicate(self.tiangatas,x=-6.6)
        self.tiangatas1  = duplicate(self.tiangkanan,x=-6.6)

        # Tiang luar
        self.tiangluarA = duplicate(self.tiangbawah,x=8.2,z=-8)
        self.tiangluarA = duplicate(self.tiangatas,x=8.2,z=-8)
        self.tiangluarT = duplicate(self.tiangkanan,x=8.2, z=-8)
        
        # Tiang luar deket ruang 4
        self.tiangluarB = duplicate(self.tiangbawah,x=8.2,z=-23.2)
        self.tiangluarA = duplicate(self.tiangatas,x=8.2,z=-23.2)
        self.tiangluarT = duplicate(self.tiangkanan,x=8.2, z=-23.2)
        
        # Kursi baris kanan
        self.kursi          = Entity(model='folding.obj', scale=(0.020), position=(2,0,1), color=color.black, collider='box', rotation = (-90,180,0))
        self.wanita_duduk   = Entity(model='img/duduk.FBX', scale=(0.015), position=(5,0.1, 0.5), color=color.light_gray, collider='box', rotation = (0,150,0))
        self.pria_duduk     = Entity(model='img/laki duduk.obj', scale=(0.060), position=(4,0,6), color=color.light_gray, collider='box', rotation = (0,-90,0))
        self.kursi2         = duplicate(self.kursi,x=3)
        self.kursi3         = duplicate(self.kursi,x=4)
        self.kursi4         = duplicate(self.kursi,x=5)
        self.kursi5         = duplicate(self.kursi,x=6)
        self.wanita         = duplicate(self.wanita_duduk, x=6)
        
        self.kursi1         = duplicate(self.kursi,x=2,z=3)
        self.kursi2         = duplicate(self.kursi,x=3,z=3)
        self.wanita         = duplicate(self.wanita_duduk, x=3,z=2.5)
        self.kursi3         = duplicate(self.kursi,x=4,z=3)
        self.wanita         = duplicate(self.wanita_duduk, x=4,z=2.5)
        self.kursi4         = duplicate(self.kursi,x=5,z=3)
        self.wanita         = duplicate(self.wanita_duduk, x=5,z=2.5)
        self.kursi5         = duplicate(self.kursi,x=6,z=3)

        self.kursi1         = duplicate(self.kursi,x=2,z=5)
        self.kursi2         = duplicate(self.kursi,x=3,z=5)
        self.kursi3         = duplicate(self.kursi,x=4,z=5)
        self.kursi4         = duplicate(self.kursi,x=5,z=5)

        self.kursi1         = duplicate(self.kursi,x=2,z=7)
        self.kursi2         = duplicate(self.kursi,x=3,z=7)
        self.kursi3         = duplicate(self.kursi,x=4,z=7)
        self.kursi4         = duplicate(self.kursi,x=5,z=7)
        self.pria           = duplicate(self.pria_duduk, x=5,z=6)
        self.kursi5         = duplicate(self.kursi,x=6,z=7)

        # Kursi baris kiri
        self.kursi1         = duplicate(self.kursi,x=-2)
        self.kursi2         = duplicate(self.kursi,x=-3)
        self.kursi3         = duplicate(self.kursi,x=-4)
        self.pria           = duplicate(self.pria_duduk, x=-3.7,z=0.3,rotation_y=-120)
        self.kursi4         = duplicate(self.kursi,x=-5)
        self.pria           = duplicate(self.pria_duduk, x=-4.7,z=0.3,rotation_y=-120)
        self.kursi5         = duplicate(self.kursi,x=-6)
        self.pria           = duplicate(self.pria_duduk, x=-5.7,z=0.3,rotation_y=-120)
        
        self.kursi1         = duplicate(self.kursi,x=-2,z=3)
        self.pria           = duplicate(self.pria_duduk, x=-1.7,z=2.3,rotation_y=-120)
        self.kursi2         = duplicate(self.kursi,x=-3,z=3)
        self.pria           = duplicate(self.pria_duduk, x=-2.7,z=2.3,rotation_y=-120)
        self.kursi3         = duplicate(self.kursi,x=-4,z=3)
        self.kursi4         = duplicate(self.kursi,x=-5,z=3)
        self.kursi5         = duplicate(self.kursi,x=-6,z=3)

        self.kursi1         = duplicate(self.kursi,x=-2,z=5)
        self.kursi2         = duplicate(self.kursi,x=-3,z=5)
        self.kursi3         = duplicate(self.kursi,x=-4,z=5)
        self.kursi4         = duplicate(self.kursi,x=-5,z=5)

        self.kursi1         = duplicate(self.kursi,x=-2,z=7)
        self.kursi2         = duplicate(self.kursi,x=-3,z=7)
        self.kursi3         = duplicate(self.kursi,x=-4,z=7)
        self.pria           = duplicate(self.pria_duduk, x=-3.7,z=6.3,rotation_y=-120)
        self.kursi4         = duplicate(self.kursi,x=-5,z=7,collider=None)
        self.kursi5         = duplicate(self.kursi,x=-6,z=7)
        self.wanita         = duplicate(self.wanita_duduk, x=-6,z=6.5,rotation_y=130)

        # Orang yg Presentasi
        self.orang1 = Entity(model='img/rp_dennis_posed_004_100k.OBJ', texture='rp_dennis_posed_004_dif.jpg', scale=(0.015), position=(3.5, 0, -3.5), double_sided=True, rotation = (0,-90,0))
        self.orang2 = Entity(model='rp_carla_rigged_001_ue4.fbx', texture='rp_carla_rigged_001_dif.jpg', scale=(0.015), position=(-4, 0, -3.5), double_sided=True, rotation = (0,30,0))
        self.orang3 = Entity(model='img/rp_manuel_animated_001_dancing.fbx', texture='rp_manuel_animated_001_dif.jpg', scale=(0.015), position=(-3, 0, -3.5), double_sided=True, rotation = (-90,30,0))
        self.orang4 = Entity(model='img/1 (1).fbx', texture='girl1_d.tga', scale=(1.5), position=(4.5, 0, -3.5), double_sided=True, rotation = (0,-40,0))

        # Peralatan depan
        self.bangku_dosen   = Entity(model='img/bangku.obj', scale=(2), position=(-5, 0, -4), color=color.black, collider='box')
        self.meja_dosen     = Entity(model='img/office_desk.obj', scale=(2), position=(-6.5, 1, -2), texture =kayu, collider='box', double_side=True)
        self.meja_mini      = Entity(model='img/3d-model.fbx', texture='wod.jpg', double_sided=True, scale=(0.05,0.05,0.030), position=(0, 0, -1.5),collider='box', rotation = (0,90,0))
        self.Infocus        = Entity(model='img/Beamer_timco.obj', color=color.light_gray, double_sided=True, scale=(0.020), position=(0, 1.4, -1.2),collider='box', rotation = (0,313,0))
        self.LP             = Entity(model='img/laptop.obj', texture='Bake_Col_3.jpg', double_sided=True,scale=(0.15), position=(-3.5, 1.45, -2.5),collider='box', rotation = (0,180,0))

        # inisialisasi posisi awal
        self.orang1_start_position = self.orang1.position

    def move_orang1(self):
        # Gerakan ke kiri
        target_position = self.orang1_start_position - Vec3(0, 0, -0.5)  # Menggerakkan ke kiri

        # Animasi gerakan ke kiri 
        self.orang1.animate_position(target_position, duration=2, curve=curve.linear)

        # Panggil kembali fungsi untuk kembali ke posisi awal setelah 2 detik
        invoke(self.move_orang1_back, delay=2)

    def move_orang1_back(self):
        # Animasi kembali ke posisi awal 
        self.orang1.animate_position(self.orang1_start_position, duration=1, curve=curve.linear)

        # Panggil kembali fungsi untuk gerakan berikutnya 
        invoke(self.move_orang1, delay=2)

    # fungsi pintu buka dan tutup
    def buka_pintu(self):
            target_position = self.pintu.position + Vec3(1, 0, 0.95)  
            target_rotation = self.pintu.rotation + Vec3(0, 90, 0) # Memutar pintu sebesar 90 derajat

            # Animasi membuka pintu
            self.pintu.animate_position(target_position, duration=2, curve=curve.linear)
            self.pintu.animate_rotation(target_rotation, duration=1, curve=curve.linear)


    def tutup_pintu(self):
            target_position = self.pintu.position - Vec3(1, 0, 0.95)# Kembali ke posisi awal
            target_rotation = self.pintu.rotation + Vec3(0, -90, 0)

            # Animasi menutup pintu
            self.pintu.animate_position(target_position, duration=2, curve=curve.linear)
            self.pintu.animate_rotation(target_rotation, duration=1, curve=curve.linear)

# Membuat instansi RuangKelas
ruang_kelas = RuangKelas()
ruang_kelas.move_orang1()
def input(key):
    if key == 'left mouse down':
        ruang_kelas.buka_pintu()
    elif key == 'right mouse down':
        ruang_kelas.tutup_pintu()

# Kamera Pemain
player = FirstPersonController(position=(-5,0,7),rotation = (0,160,0))

# Menambahkan pencahayaan position=(-5,0,7),rotation = (0,160,0)
# DirectionalLight(parent=scene, y=10, z=-10, shadows=True, color=color.white)
# AmbientLight(color=color.rgba(100, 100, 100, 0.3))  # Cahaya ambient untuk memastikan seluruh ruangan terlihat

# Menjalankan aplikasi
app.run()
