module GrayScott

export simulate

function simulate(N::Int, steps::Int, F::Float64, k::Float64)
    Du = 0.16
    Dv = 0.08
    dt = 1.0

    # Matrixes
    U = ones(Float64, N, N)
    Unext = ones(Float64, N, N)
    V = zeros(Float64, N, N)
    Vnext = zeros(Float64, N, N)

    # Small square with noise
    r = N ÷ 20 # half-width
    mid = N ÷ 2
    for i in (mid - r):(mid + r), j in (mid - r):(mid + r)
        U[i, j] = 0.5 + 0.02 * (rand() - 0.5)
        V[i, j] = 0.25 + 0.02 * (rand() - 0.5)
    end


    for step in 1:steps
        @inbounds for j in 1:N, i in 1:N
            #neighbours
            ip1 = mod1(i + 1, N)
            im1 = mod1(i - 1, N)
            jp1 = mod1(j + 1, N)
            jm1 = mod1(j - 1, N)

            lapU = U[ip1, j] + U[im1, j] + U[i, jp1] + U[i, jm1] - 4 * U[i, j]
            lapV = V[ip1, j] + V[im1, j] + V[i, jp1] + V[i, jm1] - 4 * V[i, j]

            u = U[i, j]
            v = V[i, j]
            uvv = u * v * v

            Unext[i, j] = u + dt * (Du * lapU - uvv + F * (1 - u))
            Vnext[i, j] = v + dt * (Dv * lapV + uvv - (F + k) * v)
        end

        # swap
        U, Unext = Unext, U
        V, Vnext = Vnext, V
    end
    
    return V
end

end # module