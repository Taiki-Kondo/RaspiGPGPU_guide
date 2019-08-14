import numpy as np
#np.set_printoptions(threshold=np.inf)
import time
from videocore.assembler import qpu
from videocore.driver import Driver
def mask(idx):
    values = [1]*16
    values[idx] = 0
    return values
@qpu
def pimatrix(asm):
    B_B=0
    A_B=1
    C_B=2
    STR=3
    ii=4
    THR=5
    jj=6
    THR_NM=7
    K=8
    A_ADDR=9
    B_ADDR=10
    C_ADDR=11
    COMPLETED=0

    mov(null,uniform)
    mov(r2,1)
    ldi(null,mask(B_B),set_flags=True)
    mov(r2,uniform,cond='zs')
    ldi(null,mask(A_B),set_flags=True)
    mov(r2,uniform,cond='zs')
    ldi(null,mask(C_B),set_flags=True)
    mov(r2,uniform,cond='zs')
    ldi(null,mask(STR),set_flags=True)
    mov(r2,uniform,cond='zs')
    ldi(null,mask(ii),set_flags=True)
    mov(r2,uniform,cond='zs')
    ldi(null,mask(THR),set_flags=True)
    mov(r2,uniform,cond='zs')
    ldi(null,mask(jj),set_flags=True)
    mov(r2,uniform,cond='zs')
    ldi(null,mask(THR_NM),set_flags=True)
    mov(r2,uniform,cond='zs')
    
    mov(tmu_noswap,1)
    

    L.i
    
    rotate(broadcast,r2,-A_B)
    ldi(null,mask(A_ADDR),set_flags=True)
    mov(r2,r5,cond='zs')
    
    rotate(broadcast,r2,-B_B)
    ldi(null,mask(B_ADDR),set_flags=True)
    mov(r2,r5,cond='zs')
    
    rotate(broadcast,r2,-C_B)
    ldi(null,mask(C_ADDR),set_flags=True)
    mov(r2,r5,cond='zs')
    
    rotate(broadcast,r2,-jj)
    ldi(null,mask(K),set_flags=True)
    mov(r2,r5,cond='zs')
                
    L.K
    rotate(broadcast,r2,-STR)
    imul24(r0,element_number,r5)
    rotate(broadcast,r2,-A_ADDR)
    iadd(r3,r0,r5)
    rotate(broadcast,r2,-B_ADDR)
    iadd(r1,r0,r5)
    for i in range(32):
        mov(tmu0_s,r3)
        mov(tmu1_s,r1)
        nop(sig='load tmu1')
        mov(r0,r4)
        nop(sig='load tmu0')
        fadd(ra[i],r0,r4)
        iadd(r3,r3,4)
        iadd(r1,r1,4)
        mov(tmu0_s,r3)
        mov(tmu1_s,r1)
        nop(sig='load tmu1')
        mov(r0,r4)
        nop(sig='load tmu0')    
        fadd(rb[i],r0,r4)
        iadd(r3,r3,4)
        iadd(r1,r1,4)
        

        
    mutex_acquire()
    rotate(broadcast,r2,-STR)
    setup_dma_load_stride(r5,tmp_reg=r3)
    rotate(broadcast,r2,-STR)
    ldi(r3,4*16)
    isub(broadcast,r5,r3)
    setup_dma_store_stride(r5,tmp_reg=r3)

    #block 0 set
    setup_dma_load(mode='32bit horizontal',Y=0,nrows=16,mpitch=0)
    rotate(broadcast,r2,-C_ADDR)
    start_dma_load(r5)
    mov(r3,r5)
    wait_dma_load()
    setup_vpm_read(mode='32bit vertical',Y=0,X=0,nrows=16)
    setup_vpm_write(mode='32bit vertical',Y=0,X=0)
#kokomade
    #block 1 set
    setup_dma_load(mode='32bit horizontal',Y=16,X=0,nrows=16,mpitch=0)
    ldi(broadcast,4*16)
    iadd(vpm_ld_addr,r3,r5)
    #vpm ra,rb
    mov(vpm,ra0)
    mov(vpm,rb0)
    mov(vpm,ra1)
    mov(vpm,rb1)
    mov(vpm,ra2)
    mov(vpm,rb2)
    mov(vpm,ra3)
    mov(vpm,rb3)
    mov(vpm,ra4)
    mov(vpm,rb4)
    mov(vpm,ra5)
    mov(vpm,rb5)
    mov(vpm,ra6)
    mov(vpm,rb6)
    mov(vpm,ra7)
    mov(vpm,rb7)
    
    #block0 store
    setup_dma_store(mode='32bit horizontal',Y=0,nrows=16)
    start_dma_store(r3)

    #setup vpm block1
    wait_dma_load()
    setup_vpm_read(mode='32bit vertical',Y=16,X=0,nrows=16)
    setup_vpm_write(mode='32bit vertical',Y=16,X=0)

    #set block2
    setup_dma_load(mode='32bit horizontal',Y=32,X=0,nrows=16,mpitch=0)
    ldi(r0,4*16*2)
    iadd(vpm_ld_addr,r3,r0)

    mov(vpm,ra8)
    mov(vpm,rb8)
    mov(vpm,ra9)
    mov(vpm,rb9)
    mov(vpm,ra10)
    mov(vpm,rb10)
    mov(vpm,ra11)
    mov(vpm,rb11)
    mov(vpm,ra12)
    mov(vpm,rb12)
    mov(vpm,ra13)
    mov(vpm,rb13)
    mov(vpm,ra14)
    mov(vpm,rb14)
    mov(vpm,ra15)
    mov(vpm,rb15)
    
    #store block1
    wait_dma_store()
    setup_dma_store(mode='32bit horizontal',Y=16,nrows=16)
    ldi(r0,4*16)
    iadd(vpm_st_addr,r3,r0)

    #set VPM block2
    wait_dma_load()
    setup_vpm_read(mode='32bit vertical',X=0,Y=32,nrows=16)
    setup_vpm_write(mode='32bit vertical',X=0,Y=32)

    #set block3
    setup_dma_load(mode='32bit horizontal',Y=48,X=0,nrows=16,mpitch=0)
    ldi(r0,4*16*3)
    iadd(vpm_ld_addr,r3,r0)
    
    mov(vpm,ra16)
    mov(vpm,rb16)
    mov(vpm,ra17)
    mov(vpm,rb17)
    mov(vpm,ra18)
    mov(vpm,rb18)
    mov(vpm,ra19)
    mov(vpm,rb19)
    mov(vpm,ra20)
    mov(vpm,rb20)
    mov(vpm,ra21)
    mov(vpm,rb21)
    mov(vpm,ra22)
    mov(vpm,rb22)
    mov(vpm,ra23)
    mov(vpm,rb23)
    
    #store block2
    wait_dma_store() # Wait for store of block 1
    setup_dma_store(mode='32bit horizontal', Y=32, nrows=16)
    ldi(r0, 4*16*2)
    iadd(vpm_st_addr, r3, r0)

    #set VPM block3
    wait_dma_load() # Wait for load of block 3
    setup_vpm_read(mode='32bit vertical', X=0, Y=48, nrows=16)
    setup_vpm_write(mode='32bit vertical', X=0, Y=48)

    mov(vpm,ra24)
    mov(vpm,rb24)
    mov(vpm,ra25)
    mov(vpm,rb25)
    mov(vpm,ra26)
    mov(vpm,rb26)
    mov(vpm,ra27)
    mov(vpm,rb27)
    mov(vpm,ra28)
    mov(vpm,rb28)
    mov(vpm,ra29)
    mov(vpm,rb29)
    mov(vpm,ra30)
    mov(vpm,rb30)
    mov(vpm,ra31)
    mov(vpm,rb31)

    #store block3
    wait_dma_store() # Wait for store of block 2
    setup_dma_store(mode='32bit horizontal', Y=48, nrows=16)
    ldi(r0, 4*16*3)
    iadd(vpm_st_addr, r3, r0)
    
    wait_dma_store() # Wait for store of block 3

    mutex_release()
    
    ldi(r0,64*4)
    ldi(null,mask(A_ADDR),set_flags=True)
    iadd(r2,r2,r0,cond='zs')
    ldi(null,mask(B_ADDR),set_flags=True)
    iadd(r2,r2,r0,cond='zs')
    ldi(null,mask(C_ADDR),set_flags=True)
    iadd(r2,r2,r0,cond='zs')
    rotate(broadcast,r2,-K)
    isub(r0,r5,1)
    jzc(L.K)
    ldi(null,mask(K),set_flags=True)
    mov(r2,r0,cond='zs')
    nop()

    rotate(broadcast,r2,-STR)
    ldi(r1,16)
    imul24(r0,r5,r1)
    ldi(null,mask(A_B),set_flags=True)
    iadd(r2,r2,r0,cond='zs')
    ldi(null,mask(B_B),set_flags=True)
    iadd(r2,r2,r0,cond='zs')
    ldi(null,mask(C_B),set_flags=True)
    iadd(r2,r2,r0,cond='zs')
    rotate(broadcast,r2,-ii)
    isub(r0,r5,1)
    jzc(L.i)
    ldi(null,mask(ii),set_flags=True)
    mov(r2,r0,cond='zs')
    nop()
    
#====semafo=====    
    sema_up(COMPLETED)
    rotate(broadcast,r2,-THR)
    iadd(null,r5,-1,set_flags=True)
    jzc(L.skip_fin)
    nop()
    nop()
    nop()
    rotate(broadcast,r2,-THR_NM)
    iadd(r0, r5, -1,set_flags=True)
    L.sem_down
    jzc(L.sem_down)
    sema_down(COMPLETED)    # Wait completion of all threads.
    nop()
    iadd(r0, r0, -1)
    
    interrupt()
    
    L.skip_fin
    
    exit(interrupt=False)
    
with Driver() as drv:
    i=1920
    j=1088
    n_threads=12
    A=drv.alloc((i,j),'float32')
    B=drv.alloc((i,j),'float32')
    C=drv.alloc((i,j),'float32')
    A[:,:]=1.0
    B[:,:]=1.0
    height=int(i/n_threads)
    ii=height/16
    jj=j/64
    uniforms=drv.alloc((n_threads,12),'uint32')
    uniforms[:,0]=uniforms.addresses()[:,0]
    for th in range(n_threads):
        uniforms[th,1]=B.addresses()[height*th,0]
        uniforms[th,2]=A.addresses()[height*th,0]
        uniforms[th,3]=C.addresses()[height*th,0]
    uniforms[:,4]=A.strides[0]
    uniforms[:,5]=ii
    uniforms[:,6]=np.arange(1,(n_threads+1))
    uniforms[:,7]=jj
    uniforms[:,8]=n_threads
    code=drv.program(pimatrix)
    start = time.time()
    drv.execute(
            n_threads=n_threads,
            program=code,
            uniforms=uniforms
            )
    elapsed_gpu = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_gpu) + "[sec]")
    print("{0}Gflops".format((1920*1088)/elapsed_gpu/(1000**3)))
    CA=np.zeros((i,j))
    CB=np.zeros((i,j))
    CA[:]=1.0
    CB[:]=1.0
    CC=CA+CB
    print('maximum absolute error: {:.4e}'.format(
        float(np.max(np.abs(C - CC)))))