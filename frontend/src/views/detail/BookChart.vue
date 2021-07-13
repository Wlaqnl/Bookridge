<template>
  <div>
    <mdb-row>
      <!-- {{ popular }} -->
      <mdb-col lg="8">
        <mdb-bar-chart :data="barChartData" :options="barChartOptions" :width="600" :height="300"></mdb-bar-chart>
      </mdb-col>
      <mdb-col lg="4">
        <h6 class="font-weight-bold mb-3 do">👶AGE👵</h6>
        <h3 class="font-weight-bold mb-3 p-0 do">
          <strong>연령별 선호도</strong>
        </h3>
        <p class="do">00년 00월 ~ 00년 00월 까지</p>
        <p class="do">
          19/08/2018 기준
        </p>
      </mdb-col>
    </mdb-row>
    <hr class="my-5" />
    <mdb-row>
      <mdb-col lg="4">
        <h6 class="font-weight-bold mb-3 do">👩‍💻GENDER👨‍💻</h6>
        <h3 class="font-weight-bold mb-3 p-0 do">
          <strong>성별 선호도</strong>
        </h3>
        <p class="do">00년 00월 ~ 00년 00월 까지</p>
        <p class="do">
          by
         19/08/2018 기준
        </p>
      </mdb-col>
      <mdb-col lg="8">
        <mdb-doughnut-chart
          :data="doughnutChartData"
          :options="doughnutChartOptions"
          :width="600"
          :height="300"
        ></mdb-doughnut-chart>
      </mdb-col>
    </mdb-row>
    <hr class="my-5" />
    <mdb-row>
      <mdb-col lg="8">
        <mdb-line-chart
          :data="lineChartData"
          :options="lineChartOptions"
          :width="600"
          :height="300"
        ></mdb-line-chart>
      </mdb-col>
      <mdb-col lg="4">
        <h6 class="font-weight-bold mb-3 do">📅PERIOD📉</h6>
        <h3 class="font-weight-bold mb-3 p-0 do">
          <strong>월별 선호도</strong>
        </h3>
        <p class="do">00년 00월 ~ 00년 00월 까지</p>
        <p class="do">
          by
         19/08/2018 기준
        </p>
      </mdb-col>
    </mdb-row>
    <hr class="my-5" />
  </div>
</template>

<script>
import {
  mdbBarChart,
  mdbDoughnutChart,
  mdbLineChart,
  mdbRow,
  mdbCol,
} from "mdbvue";
export default {
  name: "BookChart",
  components: {
    mdbBarChart,
    mdbDoughnutChart,
    mdbLineChart,
    mdbRow,
    mdbCol,
  },
  props: {
    popular: {
      type: Object,
    },
  },
  created() {
    console.log(this.popular.age);
    console.log("####")
    this.barChartData.datasets[0].data = this.popular.age;
    this.doughnutChartData.datasets[0].data[0] = this.popular.gender["남성"];
    this.doughnutChartData.datasets[0].data[1] = this.popular.gender["여성"];
    this.lineChartData.datasets[0].data = this.popular.date["2017"];
    this.lineChartData.datasets[1].data = this.popular.date["2018"];
    this.lineChartData.datasets[2].data = this.popular.date["2019"];
    this.lineChartData.datasets[3].data = this.popular.date["2020"];
    console.log(this.barChartData.datasets[0].data);
  },
  watch: {},
  data() {
    return {
      test: null,
      barChartData: {
        labels: [
          "8~13세",
          "14~19세",
          "20대",
          "30대",
          "40대",
          "50대",
          "60세 이상",
        ],
        datasets: [
          {
            label: ["도서대여횟수"],
            data: [0, 0, 0, 0, 0, 0, 0],
            backgroundColor: [
              "rgba(255, 99, 132, 0.2)",
              "rgba(54, 162, 235, 0.2)",
              "rgba(255, 206, 86, 0.2)",
              "rgba(75, 192, 192, 0.2)",
              "rgba(153, 102, 255, 0.2)",
              "rgba(255, 159, 64, 0.2)",
              "rgba(162,162,162,0.2)",
            ],
            borderColor: [
              "rgba(255,99,132,1)",
              "rgba(54, 162, 235, 1)",
              "rgba(255, 206, 86, 1)",
              "rgba(75, 192, 192, 1)",
              "rgba(153, 102, 255, 1)",
              "rgba(255, 159, 64, 1)",
              "rgba(162,162,162,1)",
            ],
            borderWidth: 1,
          },
        ],
      },
      barChartOptions: {
        responsive: false,
        maintainAspectRatio: false,
        scales: {
          xAxes: [
            {
              barPercentage: 1,
              gridLines: {
                display: true,
                color: "rgba(0, 0, 0, 0.1)",
              },
            },
          ],
          yAxes: [
            {
              gridLines: {
                display: true,
                color: "rgba(0, 0, 0, 0.1)",
              },
            },
          ],
        },
      },
      doughnutChartData: {
        labels: ["Man", "Woman"],
        datasets: [
          {
            data: [0, 0],
            backgroundColor: ["#46BFBD", "#F7464A"],
            hoverBackgroundColor: ["#5AD3D1", "#FF5A5E"],
          },
        ],
      },
      doughnutChartOptions: {
        responsive: false,
        maintainAspectRatio: false,
      },
      lineChartData: {
        labels: [
          "1월",
          "2월",
          "3월",
          "4월",
          "5월",
          "6월",
          "7월",
          "8월",
          "9월",
          "10월",
          "11월",
          "12월",
        ],
        datasets: [
          {
            label: "2017년",
            backgroundColor: "rgba(255, 99, 132, 0.1)",
            borderColor: "rgba(255, 99, 132, 1)",
            borderWidth: 0.7,
            data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          },
          {
            label: "2018년",
            backgroundColor: "rgba(151,187,205,0.2)",
            borderColor: "rgba(151,187,205,1)",
            borderWidth: 0.8,
            data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          },
          {
            label: "2019년",
            backgroundColor: "rgba(153, 102, 255, 0.2)",
            borderColor: "rgba(153, 102, 255, 1)",
            borderWidth: 0.7,
            data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          },
          {
            label: "2020년",
            backgroundColor: "rgba(255, 159, 64, 0.2)",
            borderColor: "rgba(255, 159, 64, 0.2)",
            borderWidth: 0.8,
            data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          },
        ],
      },
      lineChartOptions: {
        responsive: false,
        maintainAspectRatio: false,
        scales: {
          xAxes: [
            {
              gridLines: {
                display: true,
                color: "rgba(0, 0, 0, 0.1)",
              },
            },
          ],
          yAxes: [
            {
              gridLines: {
                display: true,
                color: "rgba(0, 0, 0, 0.1)",
              },
            },
          ],
        },
      },
    };
  },
};
</script>

<style scoped>
.do {
  font-family: "Do Hyeon", sans-serif;
}
</style> 