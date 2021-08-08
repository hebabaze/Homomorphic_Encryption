# Homomorphic-encryption
we had used two machines one as server (Process 1) and other as client (Process 0)
we had setup a MPI cluster

## Needed Packages
```bash
pip install MPI
pip install phe
pip install libnum
pip install mpi4py
```
how to execute with machine-file:

```bash
mpirun -hostfile machinefile -n 2 examprog
mpirun -machinefile machinefile -n 2 examprog
```

- How to Force Execution with two Machine :


```bash
 mpirun -np 2 -H master,slave ./cpi
```

- Mount NFs : 


```bash
sudo mount -t nfs master:/home/usor/cloud ~/cloud
```

- NFS restart :


```bash
sudo systemctl status nfs-kernel-server
```
## Execution Methods 
- ### In Gnu/Linux Envirnment
  **Cloud and client are machines names**  

```bash
mpirun -np 2 -H cloud,client python3 -m mpi4py pfe.py 
```

​				**Or using host file  :**

```bash
mpirun -np 2 -hostfile machines python3 -m mpi4py pfe.py
```

- ### In Windows Environment
  ```bash
  mpiexec -n 2 python -m mpi4py C:\Users\usor\Desktop\ENSIAS\pfe.py
  ```

