from types import SimpleNamespace

import numpy as np
import nrrd

from cubic_bspline_kernel import CubicBsplineKernel

def unlerp(imin, xx, imax):
    """
    imin, imax should be scalars
    return a scaler
    """
    return (xx - imin) / (imax - imin)

def lerp(omin, omax, alpha):
    """
    overloaded, either three or five arguments
    should work for both scalar and vector
    omin, omax could be scalars or vectors
    """
    return (1 - alpha) * omin + alpha * omax

def lerp(omin, omax, imin, xx, imax):
    alpha = (xx - imin) / (imax - imin)
    return (1 - alpha) * omin + alpha * omax

def quantize(vmin, val, vmax, num):
    if val <= vmin:
        return 0
    elif val >= vmax:
        return num - 1
    step = (vmax - vmin) / num
    ret = np.floor((val - vmin) / step)
    # make sure ret is below num
    return (ret == num) ? ret - 1 : ret

def construct_context(params_dict):
    """
    probe: rndProbeRgbaLit
    blend: rndBlendOver
    no levoy
    """
    context = SimpleNamespace()
    context.volume = load_volume(params_dict['fpath_volume'])
    context.kernel = CubicBsplineKernel()

    context.plane_sep = params_dict['plane_sep']
    context.num_threads = params_dict['num_threads']
    context.outside_val = params_dict['outside_val']

    context.camera = Camera(**params_dict['params_camera'])

    context.transfer_func = load_transfer_func(params_dict['fpath_lut'])
    context.transfer_func.unit_step = params_dict['unit_step']
    context.transfer_func.alpha_near_one = params_dict['alpha_near_one']

    context.light = load_light(params_dict['fpath_light'])
    context.params_light = construct_params_light()

    support = context.kernel.support
    if support & 1: # odd support
        context.idx_start = (1 - support) / 2
        context.idx_end = (support - 1) / 2
    else:
        context.idx_start = 1 - support / 2
        context.idx_end = support / 2
    context.WtoI = np.linalg.inv(ctx.volume.ItoW)
    # take upper 3x3 block of 4x4 matrix, take inverse then transpose
    mat = context.volume.ItoW[:3, :3]
    context.gradient_ItoW = np.linalg.inv(mat).T

def load_volume(fpath_volume):
    data, header = nrrd.read(fpath_volume)
    mat = np.append(header['space directions'], header['space origin'][:, np.newaxis], axis=1)
    ItoW = np.append(mat, [[0, 0, 0, 1]], axis=0)
    volume = SimpleNamespace(data=data, ItoW=ItoW)
    return volume

def load_transfer_func(fpath_lut):
    data, header = nrrd.read(fpath_lut)
    vmin = header['axis mins'][1]
    vmax = header['axis maxs'][1]
    transfer_func = SimpleNamespace(rgba=rgba, vmin=vmin, vmax=vmax, len=rgba.shape[1])
    return transfer_func

def load_light(fpath_light):
    """
    assume rgb, normalized world-space light directions
    """
    light = SimpleNamespace()
    rgb = []
    xyz = []
    with open(fpath_light, 'rt') as f:
        for line in f:
            if not line.startswith('#'): # not a comment
                color, direction, is_view_space = e.split( r'\s{2,}', line.strip())
                rgb.append([float(s) for s in color.split()])
                xyz.append([float(s) for s in direction.split()])
    light.rgb = np.hstack(rgb)
    light.xyz = np.hstack(xyz)
    light.num = len(rgb)
    return light

def construct_params_light():
    """
    Blinn Phong lighting parameters
    use defaults for now
    """
    params_light = SimpleNamespace()
    params_light.depth_color_near = np.array([[1, 1, 1]])
    params_light.depth_color_far = np.array([[1, 1, 1]])
    params_light.k_ambient = 0.2
    params_light.k_diffuse = 0.8
    params_light.k_specular = 0.1
    params_light.p_shininess = 150
    return params_light
