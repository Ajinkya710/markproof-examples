# ComfyUI + Markproof

Mark every image a ComfyUI workflow produces (invisible watermark + signed C2PA Content Credentials, for EU AI Act Article 50) with the [comfyui-markproof](https://github.com/Ajinkya710/comfyui-markproof) node pack.

1. Install the pack: ComfyUI-Manager → search **Markproof**, or
   `cd ComfyUI/custom_nodes && git clone https://github.com/Ajinkya710/comfyui-markproof`
2. Set your key **before** starting ComfyUI (it's read from the environment, never stored in the workflow):
   `export MARKPROOF_API_KEY=lt_live_...` (from https://markproof.co/dashboard)
3. Load `markproof_txt2img_api.json` (an SDXL text-to-image graph), or add **Markproof: Mark & Save** after VAE Decode in your own workflow, in place of Save Image.

**Use Mark & Save instead of Save Image:** it writes the exact marked bytes. Re-saving through Save Image re-encodes the pixels and drops the C2PA manifest. Change `ckpt_name` to a checkpoint you have.

The node outputs each image's watermark code and public verify URL. **Markproof: Verify Image** checks images for the watermark; for the C2PA manifest, drop the saved file into the [free checker](https://markproof.co/check).

To queue it from a script instead of the UI: `curl -X POST http://127.0.0.1:8188/prompt -H "Content-Type: application/json" -d "{\"prompt\": $(cat markproof_txt2img_api.json)}"`
