\ Model maxOWA_path
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  15 r1 + 2 r2 - 15 b11 - b12 - 15 b21 - b22
Subject To
 R0: x_a_b + x_a_c + x_a_d = 1
 R1: - x_a_b + x_b_d + x_b_c + x_b_e = 0
 R2: - x_a_c - x_b_c + x_c_e + x_c_f - x_d_c = 0
 R3: - x_a_d - x_b_d + x_d_c + x_d_f = 0
 R4: - x_b_e - x_c_e + x_e_g = 0
 R5: - x_c_f - x_d_f + x_f_g = 0
 R6: x_e_g + x_f_g = 1
 R7: 5 x_a_b + 10 x_a_c + 2 x_a_d + x_b_d + 4 x_b_c + 4 x_b_e + 3 x_c_e
   + x_c_f + x_d_c + 3 x_d_f + x_e_g + x_f_g + r1 - b11 <= 0
 R8: 3 x_a_b + 4 x_a_c + 6 x_a_d + 3 x_b_d + 2 x_b_c + 6 x_b_e + x_c_e
   + 2 x_c_f + 4 x_d_c + 5 x_d_f + x_e_g + x_f_g + r1 - b21 <= 0
 R9: 5 x_a_b + 10 x_a_c + 2 x_a_d + x_b_d + 4 x_b_c + 4 x_b_e + 3 x_c_e
   + x_c_f + x_d_c + 3 x_d_f + x_e_g + x_f_g + r2 - b12 <= 0
 R10: 3 x_a_b + 4 x_a_c + 6 x_a_d + 3 x_b_d + 2 x_b_c + 6 x_b_e + x_c_e
   + 2 x_c_f + 4 x_d_c + 5 x_d_f + x_e_g + x_f_g + r2 - b22 <= 0
Bounds
 r1 free
 r2 free
Binaries
 x_a_b x_a_c x_a_d x_b_d x_b_c x_b_e x_c_e x_c_f x_d_c x_d_f x_e_g x_f_g
End
