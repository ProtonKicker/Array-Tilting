### A Pluto.jl notebook ###
# v0.19.42

using Markdown
using InteractiveUtils

# ╔═╡ 3a9f4e1c-8b2d-4f7a-9c1e-3d5b6a7f8c2d
using PlutoUI, Plots

# ╔═╡ 5c8e2d4f-1a3b-4c6d-8e7f-2a4b5c6d7e8f
# ╠═╡ skip_as_script = true
#= md"""
# 4-bar Trajectory Calculations

Enter the parameters below and see the trajectory plot as theta changes.
""" =#

# ╔═╡ 7d2e9c8a-4b5a-4d6e-9f8a-1c2b3d4e5f6a
# ╠═╡ skip_as_script = true
#= md"""
## Parameters

Enter the fixed parameters:
""" =#

# ╔═╡ 8e3f9d7b-5c6a-4e7d-9f1a-2b3c4d5e6f7a
@bind x1 Slider(-10.0:0.1:10.0, default=0.0, show_value=true)
@bind y1 Slider(-10.0:0.1:10.0, default=0.0, show_value=true)

# ╔═╡ 9f4a1b2c-5d7e-4f8a-9b2c-3d4e5f6a7b8b
@bind x2 Slider(-10.0:0.1:10.0, default=5.0, show_value=true)
@bind y2 Slider(-10.0:0.1:10.0, default=0.0, show_value=true)

# ╔═╡ 1a5b2c3d-6e8f-4a1b-8d2c-9e3f4a5b6c7d
@bind b Slider(0.1:0.1:20.0, default=5.0, show_value=true)
@bind d Slider(0.1:0.1:20.0, default=5.0, show_value=true)
@bind e Slider(0.1:0.1:20.0, default=5.0, show_value=true)

# ╔═╡ 2b6c3d4e-7f9a-4b2c-8e3d-9f4a5b6c7d8e
@bind theta_start Slider(0.0:0.1:6.28, default=0.0, show_value=true)
@bind theta_end Slider(0.0:0.1:6.28, default=2*pi, show_value=true)
@bind theta_steps Slider(10:1:200, default=50, show_value=true)

# ╔═╡ 0f1a2b3c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
begin
    theta_range = range(theta_start, theta_end, length=theta_steps)
end

# ╔═╡ 3c4d5e6f-7a8b-9c0d-1e2f-3a4b5c6d7e8a
begin
    function calculate_4bar(x1, y1, x2, y2, b, d, e, theta)
        a_val = sqrt((x1 - x2)^2 + (y1 - y2)^2)
        c_val = sqrt(a_val^2 + b^2 - 2 * a_val * b * cos(theta))
        
        omega_arg = (c_val^2 + e^2 - d^2) / (2 * c_val * e)
        omega_arg = clamp(omega_arg, -1.0, 1.0)
        omega_val = asin(omega_arg)
        
        angle_ah = atan(y1 - y2, x1 - x2)
        
        s_val = x2 + b * cos(theta + angle_ah)
        t_val = y2 + b * sin(theta + angle_ah)
        
        angle_ac_arg = (b * sin(theta)) / c_val
        angle_ac_arg = clamp(angle_ac_arg, -1.0, 1.0)
        angle_ac = asin(angle_ac_arg)
        
        angle_eh = omega_val + angle_ac - angle_ah
        
        m_val = x1 + e * cos(angle_eh)
        n_val = y1 + e * sin(angle_eh)
        
        return (s=s_val, t=t_val, m=m_val, n=n_val, omega=omega_val)
    end
end

# ╔═╡ 4d5e6f7a-8b9c-0d1e-2f3a-4b5c6d7e8f9a
begin
    all_s = Float64[]
    all_t = Float64[]
    all_m = Float64[]
    all_n = Float64[]
    
    for t in theta_range
        result = calculate_4bar(x1, y1, x2, y2, b, d, e, t)
        push!(all_s, result.s)
        push!(all_t, result.t)
        push!(all_m, result.m)
        push!(all_n, result.n)
    end
end

# ╔═╡ 5e6f7a8b-9c0d-1e2f-3a4b-5c6d7e8f9a0b
begin
    p = plot(legend=:topleft, aspect_ratio=:equal, title="4-bar Trajectory")
    
    scatter!([x1, x2], [y1, y2], color=:red, label="Fixed Points", markersize=8)
    plot!(all_s, all_t, color=:blue, label="Point (s,t) trajectory", linewidth=2)
    plot!(all_m, all_n, color=:green, label="Point (m,n) trajectory", linewidth=2)
    
    if !isempty(all_s)
        plot!([all_s[end], all_m[end]], [all_t[end], all_n[end]], 
               color=:purple, label="Bar d", linewidth=2, linestyle=:dash)
    end
    
    xlabel!("X")
    ylabel!("Y")
    
    p
end

# ╔═╡ 6f7a8b9c-0d1e-2f3a-4b5c-6d7e8f9a0b1c
# ╠═╡ skip_as_script = true
#= md"""
## Verification

The distance between (s,t) and (m,n) should equal d for all theta values.
""" =#

# ╔═╡ 7a8b9c0d-1e2f-3a4b-5c6d-7e8f9a0b1
begin
    distances = Float64[]
    for i in eachindex(theta_range)
        dx = all_s[i] - all_m[i]
        dy = all_t[i] - all_n[i]
        dist = sqrt(dx^2 + dy^2)
        push!(distances, dist)
    end
    
    all_approx_equal = all(abs.(distances .- d) .< 0.01)
    
    p_verify = plot(theta_range, distances, 
                    label="Actual distance", 
                    linewidth=2, 
                    title="Verification: distance between (s,t) and (m,n)")
    hline!([d], color=:red, label="Expected (d)", linestyle=:dash)
    xlabel!("Theta")
    ylabel!("Distance")
    
    p_verify
end

# ╔═╡ 8b9c0d1e-2f3a-4b5c-6d7e-8f9a0b1c2
# ╠═╡ skip_as_script = true
#= md"""
## Summary

- **Blue line**: Trajectory of point (s,t) as theta varies
- **Green line**: Trajectory of point (m,n) as theta varies  
- **Purple dashed line**: The bar d connecting (s,t) and (m,n)
- **Red dots**: Fixed points (x1,y1) and (x2,y2)

The verification plot shows the distance between (s,t) and (m,n) should be constant and equal to d.
""" =#

# ╔═╡ 00000000-0000-0000-0000-000000000001
PLUTO_PROJECT_TOML_CONTENTS = """
[deps]
PlutoUI = "7768dfe3-7a6d-5149-a793-5174b8d43a44"
Plots = "91a5bcdd-55d7-5caf-9e0b-520d859cae80"

[compat]
PlutoUI = "~0.7"
Plots = "~1.40"
"""

# ╔═╡ 00000000-0000-0000-0000-000000000002
PLUTO_MANIFEST_TOML_CONTENTS = """
# This file is machine-generated - editing it directly is not advised

julia_version = "1.12.7"
manifest_format = "2.0"
project_hash = "71853c6197a6a7f222db0f1978c7cb232b87c5ee"

[[deps.PlutoUI]]
uuid = "7768dfe3-7a6d-5149-a793-5174b8d43a44"
version = "0.7.59"

[[deps.Plots]]
uuid = "91a5bcdd-55d7-5caf-9e0b-520d859cae80"
version = "1.40.2"
"""

# ╔═╡ Cell order:
# ╠═3a9f4e1c-8b2d-4f7a-9c1e-3d5b6a7f8c2d
# ╠═5c8e2d4f-1a3b-4c6d-8e7f-2a4b5c6d7e8f
# ╟─7d2e9c8a-4b5a-4d6e-9f8a-1c2b3d4e5f6a
# ╟─8e3f9d7b-5c6a-4e7d-9f1a-2b3c4d5e6f7a
# ╟─9f4a1b2c-5d7e-4f8a-9b2c-3d4e5f6a7b8b
# ╟─1a5b2c3d-6e8f-4a1b-8d2c-9e3f4a5b6c7d
# ╟─2b6c3d4e-7f9a-4b2c-8e3d-9f4a5b6c7d8e
# ╟─0f1a2b3c-4d5e-6f7a-8b9c-0d1e2f3a4b5c
# ╟─3c4d5e6f-7a8b-9c0d-1e2f-3a4b5c6d7e8a
# ╟─4d5e6f7a-8b9c-0d1e-2f3a-4b5c6d7e8f9a
# ╟─5e6f7a8b-9c0d-1e2f-3a4b-5c6d7e8f9a0b
# ╟─6f7a8b9c-0d1e-2f3a-4b5c-6d7e8f9a0b1c
# ╟─7a8b9c0d-1e2f-3a4b-5c6d-7e8f9a0b1
# ╟─8b9c0d1e-2f3a-4b5c-6d7e-8f9a0b1c2
# ╟─00000000-0000-0000-0000-000000000001
# ╟─00000000-0000-0000-0000-000000000002