# import xacro
# from xacrodoc import XacroDoc
# xacro_file = "./model/human_hand.urdf.xacro"
# urdf_file = "./model/human_hand.urdf"
# xac = XacroDoc.from_file(xacro_file)
# urdf_string = xac.to_urdf_file(urdf_file)

import subprocess

xacro_file = "./model/human_hand.urdf.xacro"
urdf_file = "./model/human_hand.urdf"

# Convert using the xacro CLI
subprocess.run(["xacro", xacro_file, "-o", urdf_file], check=True)

print(f"Generated URDF: {urdf_file}")