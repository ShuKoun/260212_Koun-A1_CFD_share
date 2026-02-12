import numpy as np

class KounA1_CFD_Separation_Fix:
    """
    Koun-A1 CFD Engine v6.1 (Kernel Restoration)
    - Kernel: EXACT copy of v4.0 logic (Proven Stable).
    - Fix: Correct slicing for MAC Projection.
    - Feature: Checkpointing & Rollback for A1 Governor.
    """
    def __init__(self, nx=40, ny=40, Re=1000.0, dt_init=0.04, mode='BASELINE'):
        self.nx = nx; self.ny = ny
        self.lx = 1.0; self.ly = 1.0
        self.dx = self.lx / nx; self.dy = self.ly / ny
        
        self.Re = Re; self.nu = (1.0 * self.lx) / Re
        self.dt = dt_init
        self.mode = mode
        self.rho = 1.0
        self.max_pcg_iter = 200; self.ppe_tolerance = 1e-8
        
        self.U_lid = 1.0
        
        # Fields
        self.p = np.zeros((ny, nx))
        self.u = np.zeros((ny, nx + 1))
        self.v = np.zeros((ny + 1, nx))
        self.b = np.zeros((ny, nx))
        
        # History
        self.u_prev = np.zeros_like(self.u)
        self.v_prev = np.zeros_like(self.v)
        self.p_prev = np.zeros_like(self.p)

    def save_checkpoint(self):
        self.u_prev[:] = self.u
        self.v_prev[:] = self.v
        self.p_prev[:] = self.p

    def restore_checkpoint(self):
        self.u[:] = self.u_prev
        self.v[:] = self.v_prev
        self.p[:] = self.p_prev

    def compute_norm(self, field): return np.sqrt(np.mean(field**2))

    # --- 1. Physics Operators (EXACT COPY FROM v4.0) ---
    def diffusion_u(self, u):
        u_inner = u[:, 1:-1]
        d2u_dx2 = (u[:, 2:] - 2*u_inner + u[:, :-2]) / self.dx**2
        u_pad = np.zeros((self.ny + 2, self.nx - 1))
        u_pad[1:-1, :] = u_inner; u_pad[0, :] = -u_inner[0, :]; u_pad[-1, :] = 2*self.U_lid - u_inner[-1, :]
        d2u_dy2 = (u_pad[2:, :] - 2*u_inner + u_pad[:-2, :]) / self.dy**2
        return d2u_dx2 + d2u_dy2

    def diffusion_v(self, v):
        v_inner = v[1:-1, :]
        d2v_dy2 = (v[2:, :] - 2*v_inner + v[:-2, :]) / self.dy**2
        v_pad = np.zeros((self.ny - 1, self.nx + 2))
        v_pad[:, 1:-1] = v_inner; v_pad[:, 0] = -v_inner[:, 0]; v_pad[:, -1] = -v_inner[:, -1]
        d2v_dx2 = (v_pad[:, 2:] - 2*v_inner + v_pad[:, :-2]) / self.dx**2
        return d2v_dx2 + d2v_dy2

    def advection_u(self, u, v):
        u_c = u[:, 1:-1]
        du_dx = np.where(u_c > 0, (u_c - u[:, :-2]) / self.dx, (u[:, 2:] - u_c) / self.dx)
        term1 = u_c * du_dx
        v_avg = 0.25 * (v[:-1, 1:] + v[:-1, :-1] + v[1:, 1:] + v[1:, :-1])
        u_pad = np.zeros((self.ny + 2, self.nx - 1))
        u_pad[1:-1, :] = u_c; u_pad[0, :] = -u_c[0, :]; u_pad[-1, :] = 2*self.U_lid - u_c[-1, :]
        du_dy = np.where(v_avg > 0, (u_c - u_pad[:-2, :]) / self.dy, (u_pad[2:, :] - u_c) / self.dy)
        term2 = v_avg * du_dy
        return term1 + term2

    def advection_v(self, u, v):
        v_c = v[1:-1, :]
        dv_dy = np.where(v_c > 0, (v_c - v[:-2, :]) / self.dy, (v[2:, :] - v_c) / self.dy)
        term2 = v_c * dv_dy
        u_avg = 0.25 * (u[1:, :-1] + u[1:, 1:] + u[:-1, :-1] + u[:-1, 1:])
        v_pad = np.zeros((self.ny - 1, self.nx + 2))
        v_pad[:, 1:-1] = v_c; v_pad[:, 0] = -v_c[:, 0]; v_pad[:, -1] = -v_c[:, -1]
        dv_dx = np.where(u_avg > 0, (v_c - v_pad[:, :-2]) / self.dx, (v_pad[:, 2:] - v_c) / self.dx)
        term1 = u_avg * dv_dx
        return term1 + term2

    def div_mac(self, u, v):
        return (u[:, 1:] - u[:, :-1]) / self.dx + (v[1:, :] - v[:-1, :]) / self.dy

    # --- 2. Solver Operators (EXACT COPY FROM v4.0) ---
    def apply_negative_laplacian(self, p_in):
        p = p_in.copy()
        grad_p_x = np.zeros((self.ny, self.nx + 1))
        grad_p_y = np.zeros((self.ny + 1, self.nx))
        grad_p_x[:, 1:-1] = (p[:, 1:] - p[:, :-1]) / self.dx
        grad_p_y[1:-1, :] = (p[1:, :] - p[:-1, :]) / self.dy
        lap_p = (grad_p_x[:, 1:] - grad_p_x[:, :-1]) / self.dx + \
                (grad_p_y[1:, :] - grad_p_y[:-1, :]) / self.dy
        return -lap_p

    def solve_ppe_pcg(self, p_init, b):
        p = p_init.copy(); rhs = -b; norm_rhs = self.compute_norm(rhs) + 1e-25
        Ap = self.apply_negative_laplacian(p); r = rhs - Ap; r -= np.mean(r)
        res_norm = self.compute_norm(r)
        if res_norm/norm_rhs < self.ppe_tolerance: return p, 0
        diag_A = 2.0*(1.0/self.dx**2 + 1.0/self.dy**2); inv_M = 1.0/diag_A
        z = r*inv_M; d = z.copy(); rz = np.sum(r*z)
        for k in range(1, self.max_pcg_iter+1):
            d_shift = d - np.mean(d); Ad = self.apply_negative_laplacian(d_shift)
            dAd = np.sum(d * Ad)
            if abs(dAd) < 1e-20: return p, k-1
            alpha = rz / (dAd + 1e-25)
            p += alpha*d; r -= alpha*Ad; r -= np.mean(r)
            if self.compute_norm(r)/norm_rhs < self.ppe_tolerance: return p, k
            z = r*inv_M; rz_new = np.sum(r*z); beta = rz_new/(rz + 1e-25)
            d = z + beta*d; rz = rz_new
        return p, self.max_pcg_iter

    def run_step_core(self):
        u_star = self.u.copy(); v_star = self.v.copy()
        
        diff_u = self.diffusion_u(self.u); adv_u = self.advection_u(self.u, self.v)
        u_star[:, 1:-1] += self.dt * (self.nu * diff_u - adv_u)
        
        diff_v = self.diffusion_v(self.v); adv_v = self.advection_v(self.u, self.v)
        v_star[1:-1, :] += self.dt * (self.nu * diff_v - adv_v)
        
        div_star = self.div_mac(u_star, v_star)
        self.b = (self.rho / self.dt) * (div_star - np.mean(div_star))
        self.p, iters = self.solve_ppe_pcg(self.p, self.b)
        
        # --- FIX: Correct Projection Slicing ---
        gp_x = (self.p[:, 1:] - self.p[:, :-1]) / self.dx # (ny, nx-1)
        gp_y = (self.p[1:, :] - self.p[:-1, :]) / self.dy # (ny-1, nx)
        
        self.u = u_star; self.v = v_star
        # Only update interior faces
        self.u[:, 1:-1] -= (self.dt / self.rho) * gp_x
        self.v[1:-1, :] -= (self.dt / self.rho) * gp_y
        
        div_after = self.compute_norm(self.div_mac(self.u, self.v))
        u_max = np.max(np.abs(self.u)); v_max = np.max(np.abs(self.v))
        cfl = (u_max/self.dx + v_max/self.dy) * self.dt
        
        return cfl, div_after, iters

    def run_simulation(self, steps=200):
        print(f"--> Running Mode: {self.mode} | Re={self.Re}, dt_init={self.dt}")
        print(f"{'Step':<5} | {'dt':<8} | {'CFL':<6} | {'Div':<8} | {'PCG':<4} | {'Event'}")
        print("-" * 65)
        
        for step in range(1, steps+1):
            self.save_checkpoint()
            
            retry_count = 0
            while True:
                try:
                    cfl, div, iters = self.run_step_core()
                    
                    if np.isnan(div) or div > 1e-4: raise ValueError(f"Div Drift ({div:.1e})")
                    
                    if self.mode == 'BASELINE':
                        if cfl > 1.5: raise ValueError(f"CFL Blowup ({cfl:.2f})")
                        if step % 20 == 0 or step < 5:
                            print(f"{step:<5} | {self.dt:.4f}   | {cfl:.2f}   | {div:.1e} | {iters:<4} | OK")
                        break 
                        
                    elif self.mode == 'A1_GOVERNOR':
                        if cfl > 1.0: 
                            if retry_count >= 5: raise ValueError("Governor Failed: Too many retries")
                            print(f"{step:<5} | {self.dt:.4f}   | {cfl:.2f}   | {div:.1e} | {iters:<4} | >> CFL > 1.0, RETRY dt*0.5")
                            self.restore_checkpoint()
                            self.dt *= 0.5
                            retry_count += 1
                            continue 
                        
                        if step % 20 == 0 or step < 5 or retry_count > 0:
                            print(f"{step:<5} | {self.dt:.4f}   | {cfl:.2f}   | {div:.1e} | {iters:<4} | A1 Safe")
                        break
                        
                except ValueError as e:
                    print(f"{step:<5} | {self.dt:.4f}   | ERROR    | ERROR    | ---- | KILLED: {str(e)}")
                    return

def run_contrast_fix():
    print("=== Koun-A1-CFD Separation Experiment (Fixed) ===")
    print("Scenario: Re=1000, Initial dt=0.04 (Known Kill Zone)")
    print("=================================================\n")
    
    # 1. Baseline
    baseline = KounA1_CFD_Separation_Fix(mode='BASELINE')
    baseline.run_simulation()
    
    print("\n" + "="*40 + "\n")
    
    # 2. A1 Governor
    a1 = KounA1_CFD_Separation_Fix(mode='A1_GOVERNOR')
    a1.run_simulation()

if __name__ == "__main__":
    run_contrast_fix()