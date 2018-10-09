import sys

if sys.platform.startswith('linux'):
    import re
    
    try:
        with open('/proc/cpuinfo', 'r') as fp:
            cpuinfo = fp.read()
    except OSError:
        raise ImportError('AVX2 support could not be determined')

    if re.search(r'^flags\s*:.* avx2', cpuinfo, re.M):
        from . import _imaging
    else:
        raise ImportError('AVX2 not supported')
elif sys.platform == 'darwin':
    import subprocess

    try:
        sysctl_result = subprocess.run(['/usr/sbin/sysctl', '-n', 'hw.optional.avx2_0'],
                                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                       encoding='ascii')
    except OSError:
        raise ImportError('AVX2 support could not be determined')
        
    if sysctl_result.returncode != 0:
        raise ImportError(
            f'AVX2 support could not be determined (sysctl returned {sysctl_result.returncode}')

    output = sysctl_result.stdout.strip()
    if output == '1':
        from . import _imaging
    else:
        raise ImportError('AVX2 not supported')
else:
    raise ImportError('AVX2 support check not supported on this platform')

