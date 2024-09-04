<script>
    import "../../app.css";
    let img_arr = [
        "../src/pictures/img1.png",
        "../src/pictures/img2.png",
        "../src/pictures/img3.png",
        "../src/pictures/img4.png",
        "../src/pictures/img5.png",
        "../src/pictures/img6.png",
    ];
</script>

<div class="hero bg-base-200 pt-28 pb-18">
    <div class="hero-content text-center">
        <div class="max-w-md">
            <h1 class="text-5xl font-bold">
                Hyperspectral Anomaly Detection: A Powerful Tool for Data
                Analysis
            </h1>
            <div class="flex flex-col gap-4 my-10 justify-center items-center">
                <input
                    type="file"
                    class="file-input file-input-bordered file-input-primary w-full max-w-xs"
                />
                <button class="btn btn-primary btn-wide text-lg">Submit</button>
            </div>
            <div class="divider"></div>
            <div class="">
                <p class="text-5xl font-bold pb-6">Output</p>
                <p class="text-lg">The output images will appear here</p>
            </div>
            <div class="divider"></div>
        </div>
    </div>
</div>
<div class="bg-base-200 flex flex-col items-center pb-20">
    <p class="font-bold text-5xl py-6">Examples</p>
    <div class="flex flex-row gap-10 mx-32 justify-center flex-wrap">
        {#each img_arr as img}
            <div class="card bg-base-100 w-96 shadow-xl">
                <figure class="px-10 pt-10">
                    <img
                        src={img}
                        alt="hyperspectral images"
                        class="rounded-xl"
                    />
                </figure>
                <div class="card-body items-center text-center">
                    <div class="card-actions">
                        <button class="btn btn-primary btn-wide text-lg"
                            >Select</button
                        >
                    </div>
                </div>
            </div>
        {/each}
    </div>
</div>
