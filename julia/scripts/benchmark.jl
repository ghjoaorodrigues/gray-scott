using Pkg
Pkg.activate(joinpath(@__DIR__, ".."))

include(joinpath(@__DIR__, "..", "src", "GrayScott.jl"))
using .GrayScott
using BenchmarkTools

const N = 256
const STEPS = 5000
const F = 0.060
const k = 0.062

function main()
    println("Benchmarking simulate(N=$N, steps=$STEPS, F=$F, k=$k)...")

    result = @benchmark simulate($N, $STEPS, $F, $k) samples=5 evals=1 seconds=60

    display(result)
    println()
    println("median: $(BenchmarkTools.prettytime(median(result).time))")
    println("min:    $(BenchmarkTools.prettytime(minimum(result).time))")
end

main()