import streamlit as st
import subprocess
import os

# ✅ SET THE CORRECT AutoDock Vina PATH
VINA_PATH = r"C:\Program Files (x86)\The Scripps Research Institute\Vina\vina.exe"

# ✅ FUNCTION TO RUN VINA DOCKING
def run_vina(receptor, ligand, center_x, center_y, center_z, size_x, size_y, size_z):
    if not os.path.exists(VINA_PATH):
        return "❌ Error: AutoDock Vina executable not found. Check the path!"

    output_pdbqt = "docked_output.pdbqt"
    log_file = "vina_log.txt"

    # Docking command
    command = f'"{VINA_PATH}" --receptor {receptor} --ligand {ligand} ' \
              f'--center_x {center_x} --center_y {center_y} --center_z {center_z} ' \
              f'--size_x {size_x} --size_y {size_y} --size_z {size_z} ' \
              f'--out {output_pdbqt} --log {log_file}'

    try:
        process = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=os.getcwd())

        # ✅ CHECK OUTPUT FILES
        if os.path.exists(output_pdbqt) and os.path.exists(log_file):
            with open(log_file, "r") as log:
                vina_log = log.read()
            return vina_log  # Return log content
        else:
            return "❌ Error: Docking did not produce an output file."

    except Exception as e:
        return f"❌ Error: Docking failed.\n\n🔎 Vina Error Log:\n{str(e)}"


# ✅ STREAMLIT UI
st.title("🧬 Molecular Docking with AutoDock Vina")

# 📂 Upload receptor and ligand files
receptor_file = st.file_uploader("📥 Upload Receptor (PDBQT)", type=["pdbqt"])
ligand_file = st.file_uploader("📥 Upload Ligand (PDBQT)", type=["pdbqt"])

# 📌 Define docking parameters
st.subheader("Define Docking Box")
center_x = st.number_input("Center X", value=0.0)
center_y = st.number_input("Center Y", value=0.0)
center_z = st.number_input("Center Z", value=0.0)
size_x = st.number_input("Size X (Å)", value=20.0)
size_y = st.number_input("Size Y (Å)", value=20.0)
size_z = st.number_input("Size Z (Å)", value=20.0)

# ✅ RUN DOCKING
if st.button("🚀 Run Docking"):
    if receptor_file and ligand_file:
        receptor_path = "receptor.pdbqt"
        ligand_path = "ligand.pdbqt"

        with open(receptor_path, "wb") as f:
            f.write(receptor_file.getbuffer())
        with open(ligand_path, "wb") as f:
            f.write(ligand_file.getbuffer())

        with st.spinner("🕒 Running docking... Please wait."):
            vina_log = run_vina(receptor_path, ligand_path, center_x, center_y, center_z, size_x, size_y, size_z)

        if "Error" in vina_log:
            st.error(vina_log)
        else:
            st.success("✅ Docking completed successfully!")
            st.text_area("Vina Output", vina_log, height=300)

            with open("docked_output.pdbqt", "r") as out_file:
                docked_result = out_file.read()
            st.download_button("📥 Download Docked Output", docked_result, file_name="docked_output.pdbqt")

            with open("vina_log.txt", "r") as log_file:
                vina_log_text = log_file.read()
            st.download_button("📥 Download Log File", vina_log_text, file_name="vina_log.txt")
    else:
        st.error("⚠️ Please upload both receptor and ligand files.")
