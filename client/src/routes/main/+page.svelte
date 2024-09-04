<script lang="js">
    import "../../app.css";
    import { data } from "./data.js";

    // Function to convert base64 image data to image source
    const getImageSrc = (meow) => `data:image/png;base64,${meow}`;

    // Array of image paths
    let img_arr = [
        "../src/pictures/img1.png",
        "../src/pictures/img2.png",
        "../src/pictures/img3.png",
        "../src/pictures/img4.png",
        "../src/pictures/img5.png",
        "../src/pictures/img6.png",
    ];

    // Array to hold the images
    let images = [];
    let error = null;
    let isLoading = false;

    async function fetchData() {
        // Reset state before fetching new data
        images = [];
        error = null;
        isLoading = true;

        try {
            const response = await fetch("http://127.0.0.1:8000/analyse");
            if (response.ok) {
                const data = await response.json();
                images = data.images;
            } else {
                error = `Error: ${response.status} ${response.statusText}`;
            }
        } catch (err) {
            error = `Error: ${err.message}`;
        } finally {
            isLoading = false;
        }
    }
</script>

<div class="flex w-full h-screen">
    <!-- Left side: Hero Section -->
    <div
        class="w-6/12 bg-cover bg-center relative flex items-center justify-center"
        style="background-image: url('../src/pictures/earth.avif');"
    >
        <div class="absolute inset-0 bg-black opacity-50"></div>
        <div
            class="card flex flex-col items-center justify-center h-full w-full px-4 relative z-10"
        >
            <div class="hero flex-grow flex items-center">
                <div class="hero-content text-center">
                    <div class="max-w-lg">
                        <h1
                            class="text-5xl font-bold text-white bg-clip-text text-transparent text-center"
                        >
                            {#if isLoading}
                                <p>Loading data...</p>
                            {:else if error}
                                {#each data as image, index}
                                    <div
                                        class="relative overflow-hidden rounded-lg shadow-lg transition-transform duration-300 ease-in-out transform hover:scale-105"
                                    >
                                        <img
                                            src={getImageSrc(image)}
                                            alt={`Processed Image ${index + 1}`}
                                            class="w-full h-full object-cover"
                                        />
                                        <div
                                            class="absolute inset-0 bg-black bg-opacity-70 flex items-center justify-center text-white text-xl opacity-0 transition-opacity duration-500 ease-in-out hover:opacity-100"
                                        >
                                            <p>Image {index + 1}</p>
                                        </div>
                                    </div>
                                {/each}
                            {:else if images !== null}
                                <div class="images-container">
                                    {#each images as image}
                                        <img
                                            src={getImageSrc(image)}
                                            alt="Processed "
                                        />
                                    {/each}
                                </div>
                            {/if}
                            {#if isLoading == false}
                                Hyperspectral Anomaly Detection: A Powerful Tool
                                for Data Analysis
                            {/if}
                        </h1>
                    </div>
                </div>
            </div>
            <div
                class="flex flex-col gap-4 items-center justify-center w-full max-w-xs mb-6"
            >
                <input
                    type="file"
                    class="file-input file-input-success file-input-lg w-full"
                />
                <button
                    class="btn btn-xs sm:btn-sm md:btn-md lg:btn-lg btn-outline btn-success w-full"
                >
                    Submit
                </button>
            </div>
        </div>
    </div>

    <div class=""></div>
    <div class="card h-screen w-6/12 flex flex-col">
        <h1 class="text-5xl font-bold flex flex-row justify-center mb-6 mt-6">
            Examples
        </h1>
        <div class="flex-grow overflow-y-auto px-4">
            <div
                class="flex flex-row flex-wrap items-start justify-center gap-10 pb-6"
            >
                {#each img_arr as img}
                    <div class="card bg-base-100 w-96 shadow-xl">
                        <figure>
                            <img src={img} alt="Shoes" />
                        </figure>
                        <div class="card-body">
                            <div class="card-actions justify-center">
                                <button
                                    on:click={fetchData}
                                    class="btn btn-success">Select</button
                                >
                            </div>
                        </div>
                    </div>
                {/each}
            </div>
        </div>
    </div>
</div>

<style>
    .images-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }

    img {
        max-width: 200px;
        border: 1px solid #ccc;
        padding: 5px;
    }
</style>
