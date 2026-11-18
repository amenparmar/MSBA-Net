"""Efficiency of all eight models in ONE session (same method as final_tests.py: FP32, batch 1, 256x256x1, binary
output, 50 warm-up + 300 timed runs, median; GMACs from PyTorch's FLOP counter). Must run on an otherwise idle GPU.
Writes the key "latency" into v2c_stats.json."""
import os, sys, json, time
sys.dont_write_bytecode = True
import numpy as np, torch
from torch.utils.flop_counter import FlopCounterMode
import common as C

MODELS = ["UNet", "UNetPlusPlus", "AttUNet", "DeepLabV3Plus", "HRNetW18", "SegFormerB1", "MSBANet", "MSBANetV2c"]
util = os.popen("nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits").read().strip()
print("GPU utilisation before timing:", util, "%")
eff = {}
for m in MODELS:
    net = C.MODELS[m](1).eval(); x = torch.randn(1, 1, 256, 256)
    with FlopCounterMode(display=False) as fc, torch.no_grad():
        net(x)
    net = net.to(C.DEV); xg = x.to(C.DEV); ts = []
    with torch.no_grad():
        for _ in range(50):
            net(xg)
        for _ in range(300):
            torch.cuda.synchronize(); t = time.perf_counter(); net(xg); torch.cuda.synchronize()
            ts.append((time.perf_counter() - t) * 1000)
    eff[m] = {"params_M": sum(p.numel() for p in net.parameters()) / 1e6, "gmacs": fc.get_total_flops() / 2e9,
              "latency_ms": float(np.median(ts))}
    print(m, {k: round(v, 2) for k, v in eff[m].items()}, flush=True)
    del net; torch.cuda.empty_cache()
p = os.path.join(C.HERE, "v2c_stats.json"); d = json.load(open(p)); d["latency"] = eff
d["latency_meta"] = {"gpu_util_before_pct": util, "time": time.strftime("%Y-%m-%d %H:%M:%S")}
json.dump(d, open(p, "w"), indent=1)
