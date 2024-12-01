\ Model maxmin_path
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  y
Subject To
 R0: x_a_b + x_a_c = 1
 R1: - x_a_b + x_b_c + x_b_e + x_b_f + x_b_d = 0
 R2: - x_a_c - x_b_c + x_c_e + x_c_d = 0
 R3: - x_b_d - x_c_d + x_d_f = 0
 R4: - x_b_e - x_c_e + x_e_f = 0
 R5: x_b_f + x_d_f + x_e_f = 1
 R6: 4 x_a_b + 5 x_a_c + 2 x_b_c + 2 x_b_e + 7 x_b_f + x_b_d + 2 x_c_e
   + 5 x_c_d + 3 x_d_f + 5 x_e_f + y <= 0
 R7: 3 x_a_b + x_a_c + x_b_c + 2 x_b_e + 5 x_b_f + 4 x_b_d + 7 x_c_e
   + x_c_d + 2 x_d_f + 2 x_e_f + y <= 0
Bounds
 -infinity <= y <= 0
Binaries
 x_a_b x_a_c x_b_c x_b_e x_b_f x_b_d x_c_e x_c_d x_d_f x_e_f
End
