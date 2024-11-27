\ Model model2
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  2 r2 - b12 - b22 - b32 - b42 - b52 - b62
Subject To
 R0: r2 - b12 <= 2
 R1: r2 - b22 <= 9
 R2: r2 - b32 <= 6
 R3: r2 - b42 <= 8
 R4: r2 - b52 <= 5
 R5: r2 - b62 <= 4
Bounds
End
