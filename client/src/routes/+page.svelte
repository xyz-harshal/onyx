<script>
    import "../app.css";
    import { onMount } from "svelte";
    import { fade } from "svelte/transition";

    let visible = false;

    onMount(() => {
        visible = true;
    });
</script>

<main class="container mx-auto px-4 py-12 max-w-6xl">
    {#if visible}
        <div in:fade={{ duration: 1000, delay: 200 }}>
            <h1 class="text-5xl font-bold mb-8 text-center text-blue-600">
                Hyperspectral Image Anomaly Detection
            </h1>

            <section
                class="mb-16 bg-gray-50 p-8 rounded-lg shadow-lg"
                in:fly={{ y: 50, duration: 1000, delay: 400 }}
            >
                <h2 class="text-3xl font-semibold mb-6 text-blue-800">
                    How Anomaly Detection Works
                </h2>
                <p class="mb-6 text-lg">
                    Our advanced system utilizes cutting-edge techniques to
                    detect anomalies in hyperspectral images:
                </p>
                <ul class="list-disc list-inside space-y-4 text-lg">
                    <li>
                        <span class="font-semibold"
                            >Optimize Anomaly Detection:</span
                        > We develop and refine Deep Learning models for accurate
                        detection of anomalies in hyperspectral images.
                    </li>
                    <li>
                        <span class="font-semibold"
                            >Enhance Data Processing:</span
                        > We apply noise reduction, data fusion, and calibration
                        to improve data quality.
                    </li>
                    <li>
                        <span class="font-semibold"
                            >Advanced Feature Extraction:</span
                        > We use dimensionality reduction and deep learning (Image
                        Processing, KNNs) for effective feature extraction and anomaly
                        detection.
                    </li>
                    <li>
                        <span class="font-semibold"
                            >Develop Target Detection Methods:</span
                        > We create methodologies to identify and classify targets
                        based on detected anomalies.
                    </li>
                </ul>
            </section>

            <section
                class="mb-16 bg-blue-50 p-8 rounded-lg shadow-lg"
                in:fly={{ y: 50, duration: 1000, delay: 600 }}
            >
                <h2 class="text-3xl font-semibold mb-6 text-blue-800">
                    Our Unique Approach
                </h2>
                <ul class="list-disc list-inside space-y-4 text-lg">
                    <li>
                        K-means clustering and SOMP comprehensive dictionaries
                        for rich feature utilization
                    </li>
                    <li>
                        Low-Rank and Sparse Representation (LRSR) to decompose
                        data into useful components
                    </li>
                    <li>
                        Incorporation of spatial correlations in dictionary
                        construction for improved accuracy
                    </li>
                    <li>
                        Focus on relevant spectral bands and efficient
                        optimization techniques
                    </li>
                </ul>
            </section>

            <section
                class="mb-16 bg-green-50 p-8 rounded-lg shadow-lg"
                in:fly={{ y: 50, duration: 1000, delay: 800 }}
            >
                <h2 class="text-3xl font-semibold mb-6 text-blue-800">
                    Key Features
                </h2>
                <ul class="list-disc list-inside space-y-4 text-lg">
                    <li>
                        Support for NASA and ISRO hyperspectral datasets
                        (AVIRIS-NG and Hyperion)
                    </li>
                    <li>Geolocation access for analyzing specific locations</li>
                    <li>Detailed anomaly reports with clear classifications</li>
                    <li>Advanced tools for experts and educational examples</li>
                </ul>
            </section>

            <section
                class="mb-16"
                in:fly={{ y: 50, duration: 1000, delay: 1000 }}
            >
                <h2 class="text-3xl font-semibold mb-6 text-blue-800">
                    Applications
                </h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div
                        class="bg-yellow-50 p-6 rounded-lg shadow-lg transition-all duration-300 hover:shadow-xl hover:scale-105"
                    >
                        <h3 class="text-2xl font-semibold mb-4 text-blue-700">
                            Military
                        </h3>
                        <p class="text-lg">
                            Enhanced target detection and surveillance
                            capabilities
                        </p>
                    </div>
                    <div
                        class="bg-red-50 p-6 rounded-lg shadow-lg transition-all duration-300 hover:shadow-xl hover:scale-105"
                    >
                        <h3 class="text-2xl font-semibold mb-4 text-blue-700">
                            Disaster Response
                        </h3>
                        <p class="text-lg">
                            Improved identification and assessment of affected
                            areas and survivors
                        </p>
                    </div>
                    <div
                        class="bg-green-50 p-6 rounded-lg shadow-lg transition-all duration-300 hover:shadow-xl hover:scale-105"
                    >
                        <h3 class="text-2xl font-semibold mb-4 text-blue-700">
                            Agriculture
                        </h3>
                        <p class="text-lg">
                            Better monitoring of crop health and detection of
                            plant diseases
                        </p>
                    </div>
                    <div
                        class="bg-blue-50 p-6 rounded-lg shadow-lg transition-all duration-300 hover:shadow-xl hover:scale-105"
                    >
                        <h3 class="text-2xl font-semibold mb-4 text-blue-700">
                            Soil Analysis
                        </h3>
                        <p class="text-lg">
                            Accurate assessment of soil composition and quality
                        </p>
                    </div>
                </div>
            </section>

            <div class="text-center" in:fade={{ duration: 1000, delay: 1200 }}>
                <a
                    href="/main"
                    class="inline-block bg-blue-600 text-white text-xl font-semibold py-4 px-8 rounded-full shadow-lg hover:bg-blue-700 hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                >
                    Try Hyperspectral Anomaly Detection
                </a>
            </div>
        </div>
    {/if}
</main>

<style>
    :global(body) {
        font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
        color: #333;
        background-color: #f0f4f8;
    }
</style>
