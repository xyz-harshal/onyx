<script lang="ts">
    import "../../app.css";
    import { data } from "./data.js";
    let img_arr = [
        "../src/pictures/img1.png",
        "../src/pictures/img2.png",
        "../src/pictures/img3.png",
        "../src/pictures/img4.png",
        "../src/pictures/img5.png",
        "../src/pictures/img6.png",
    ];
    const getImageSrc = (meow: string) => `data:image/png;base64,${meow}`;
</script>

<div
    style="background-image: url('../src/pictures/earth.avif'); background-size: cover; padding: 20px;"
    class="hero bg-base-200 pt-28 pb-18"
>
    <div class="hero-content text-center">
        <div class="max-w-6xl">
            <div>
                <h1 class="text-5xl font-bold py-32 text-white">
                    Hyperspectral Anomaly Detection: A Powerful Tool for Data
                    Analysis
                </h1>
                <div
                    class="flex flex-col gap-4 my-10 justify-center items-center"
                >
                    <input
                        type="file"
                        class="file-input file-input-bordered file-input-primary w-full max-w-xs"
                    />
                    <button class="btn btn-primary btn-wide text-lg"
                        >Submit</button
                    >
                </div>
            </div>
        </div>
    </div>
</div>
<div class="flex flex-col bg-base-200 items-center px-32">
    <p class="text-5xl font-bold pb-6">Output</p>
    {#if data}
        <div class="flex flex-row flex-wrap gap-6 justify-center">
            {#each data.images as item}
                <!-- The button to open modal -->
                <a href="#my_modal_8"
                    ><img
                        src={getImageSrc(item)}
                        alt=""
                        width="400"
                        height="400"
                        class="rounded-xl"
                    /></a
                >

                <!-- Put this part before </body> tag -->
                <div class="modal" role="dialog" id="my_modal_8">
                    <div class="modal-box">
                        <img
                            src={getImageSrc(item)}
                            alt=""
                            width="1000"
                            height="1000"
                            class="rounded-xl"
                        />
                        <div class="modal-action">
                            <a href="#" class="btn">Close</a>
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    {:else}
        <p class="text-lg">The output images will appear here</p>
    {/if}
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
