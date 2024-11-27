\ Model model4
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  4 r4 - b14 - b24 - b34 - b44 - b54 - b64
Subject To
 R0: r4 - b14 <= 2
 R1: r4 - b24 <= 9
 R2: r4 - b34 <= 6
 R3: r4 - b44 <= 8
 R4: r4 - b54 <= 5
 R5: r4 - b64 <= 4
Bounds
End
