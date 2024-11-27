\ Model model1
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  r1 - b11 - b21 - b31 - b41 - b51 - b61
Subject To
 R0: r1 - b11 <= 2
 R1: r1 - b21 <= 9
 R2: r1 - b31 <= 6
 R3: r1 - b41 <= 8
 R4: r1 - b51 <= 5
 R5: r1 - b61 <= 4
Bounds
End
