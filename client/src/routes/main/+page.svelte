<script>
    import "../../app.css";
</script>

<div class="flex w-full h-screen">
    <!-- Left side: Hero Section -->
    <div class="w-6/12 bg-cover bg-center relative flex items-center justify-center" style="background-image: url('../src/pictures/earth.avif');">
      <div class="absolute inset-0 bg-black opacity-50"></div>
      <div class="card flex flex-col items-center justify-center h-full w-full px-4 relative z-10">
        <div class="hero flex-grow flex items-center">
          <div class="hero-content text-center">
            <div class="max-w-lg">
              <h1 class="text-5xl font-bold bg-gradient-to-r from-green-500 to-green-700 bg-clip-text text-transparent text-center">
                Hyperspectral Anomaly Detection: A Powerful Tool for Data Analysis
              </h1>
            </div>
          </div>
        </div>
        <div class="flex flex-col gap-4 items-center justify-center w-full max-w-xs mb-6">
          <input
            type="file"
            class="file-input file-input-success file-input-lg w-full"
          />
          <button
            class="btn btn-xs sm:btn-sm md:btn-md lg:btn-lg btn-outline btn-success w-full"
          >Submit</button>
        </div>
      </div>
    </div>

    <div class="divider divider-horizontal"></div>
    <div class="card h-screen w-6/12 flex flex-col bg-blue-800">
        <!-- <kbd class="kbd kbd-lg mb-6 mt-6 self-center">Characteristics</kbd> -->
        <h1 class="text-5xl font-bold flex flex-row justify-center mb-6 mt-6">
            Characteristics
        </h1>
        <div class="flex-grow overflow-y-auto px-4">
            <div
                class="flex flex-row flex-wrap items-start justify-center gap-10 pb-6"
            >
            <div class="card bg-base-100 w-96 shadow-xl">
                <figure>
                    <img
                        src="../src/pictures/img1.png"
                        alt="Shoes"
                    />
                </figure>
                <div class="card-body">
                    <div class="card-actions justify-center">
                        <button class="btn btn-success">Select</button>
                    </div>
                </div>
            </div>
                <div class="card bg-base-100 w-96 shadow-xl">
                    <figure>
                        <img
                            src="../src/pictures/img4.png"
                            alt="Image1"
                        />
                    </figure>
                    <div class="card-body">
                        <div class="card-actions justify-center">
                            <button class="btn btn-success">Select</button>
                        </div>
                    </div>
                </div>
                <div class="card bg-base-100 w-96 shadow-xl">
                    <figure>
                        <img
                            src="../src/pictures/img2.png"
                            alt="image2"
                        />
                    </figure>
                    <div class="card-body">
                        <div class="card-actions justify-center">
                            <button class="btn btn-success">Select</button>
                        </div>
                    </div>
                </div>
                <div class="card bg-base-100 w-96 shadow-xl">
                    <figure>
                        <img
                            src="../src/pictures/img3.png"
                            alt="image3"
                        />
                    </figure>
                    <div class="card-body">
                        <div class="card-actions justify-center">
                            <button class="btn btn-success">Select</button>
                        </div>
                    </div>
                </div>
                <div class="card bg-base-100 w-96 shadow-xl">
                    <figure>
                        <img
                            src="../src/pictures/img5.png"
                            alt="Image5"
                        />
                    </figure>
                    <div class="card-body">
                        <div class="card-actions justify-center">
                            <button class="btn btn-success">Select</button>
                        </div>
                    </div>
                </div>
                <div class="card bg-base-100 w-96 shadow-xl">
                    <figure>
                        <img
                            src="../src/pictures/img6.png"
                            alt="Image6"
                        />
                    </figure>
                    <div class="card-body">
                        <div class="card-actions justify-center">
                            <button class="btn btn-success">Select</button>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </div>
</div>
