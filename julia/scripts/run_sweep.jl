using Pkg
Pkg.activate(joinpath(@__DIR__, ".."))

include(joinpath(@__DIR__, "..", "src", "GrayScott.jl"))
using .GrayScott

const N = 256
const STEPS = 5000

const F_VALUES = range(0.030, 0.062, length=4)
const K_VALUES = range(0.055, 0.065, length=4)

# gray-scott/output/
const OUTDIR = joinpath(@__DIR__, "..", "..", "output", "julia")
isdir(OUTDIR) || mkpath(OUTDIR)

function main()
    manifest_path = joinpath(OUTDIR, "manifest.csv")
    open(manifest_path, "w") do manifest
        println(manifest, "index,F,k,filename")

        idx = 0
        for F in F_VALUES, k in K_VALUES
            idx += 1
            Fr, kr = round(F, digits=3), round(k, digits=3)
            print("[$idx/16] F =$Fr, k=$kr ... ")

            t0 = time()
            V = simulate(N, STEPS, Float64(F), Float64(k))
            elapsed = time() - t0

            fname = "V_F$(Fr)_k$(kr).bin"
            # write() serializes Julia's native column-major layout
            # plot.py must read it back with reshape(N, N, order='F')
            open(joinpath(OUTDIR, fname), "w") do io 
                write(io, V)
            end

            println("done in $(round(elapsed, digits=2))s -> $fname")
            println(manifest, "$idx,$Fr,$kr,$fname")
        end
    end

    println("\nWrote 16 V-grids + manifest.csv to $(OUTDIR)")
end

main()