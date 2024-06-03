<template>
    <div id="schedule-grid">
      <div
        class="schedule-cell-row-header"
        :class="{ selected: isAllSelected }"
        @click="toggleAll"
      ></div>
      <div
        v-for="(day, index) in days"
        :key="day"
        class="schedule-cell-column-header"
        :class="{ selected: selectedDays[index] }"
        @click="toggleDay(index)"
      >
        {{ day }}
      </div>
      <div v-for="(period, periodIndex) in periods" :key="'period-' + periodIndex">
        <div
          class="schedule-cell-row-header"
          :class="{ selected: selectedPeriods[periodIndex] }"
          @click="togglePeriod(periodIndex)"
        >
          {{ period }}
        </div>
        <div v-for="(day, dayIndex) in days" :key="day + '-' + period">
          <div
            class="schedule-cell"
            :class="{ selected: selectedCells[dayIndex][periodIndex] }"
            @click="toggleCell(dayIndex, periodIndex)"
          ></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Timetable',
    data() {
      return {
        days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        periods: [1, 2, 3, 4, 5, 6],
        selectedDays: Array(7).fill(false),
        selectedPeriods: Array(6).fill(false),
        selectedCells: Array(7).fill(null).map(() => Array(6).fill(false)),
        isAllSelected: false,
      };
    },
    methods: {
      toggleAll() {
        this.isAllSelected = !this.isAllSelected;
        for (let i = 0; i < this.days.length; i++) {
          this.selectedDays[i] = this.isAllSelected;
          for (let j = 0; j < this.periods.length; j++) {
            this.selectedCells[i][j] = this.isAllSelected;
          }
        }
        this.selectedPeriods.fill(this.isAllSelected);
      },
      toggleDay(dayIndex) {
        this.selectedDays[dayIndex] = !this.selectedDays[dayIndex];
        for (let i = 0; i < this.periods.length; i++) {
          this.selectedCells[dayIndex][i] = this.selectedDays[dayIndex];
        }
      },
      togglePeriod(periodIndex) {
        this.selectedPeriods[periodIndex] = !this.selectedPeriods[periodIndex];
        for (let i = 0; i < this.days.length; i++) {
          this.selectedCells[i][periodIndex] = this.selectedPeriods[periodIndex];
        }
      },
      toggleCell(dayIndex, periodIndex) {
        this.$set(this.selectedCells[dayIndex], periodIndex, !this.selectedCells[dayIndex][periodIndex]);
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add your styles here */
  .schedule-cell, .schedule-cell-row-header, .schedule-cell-column-header {
    display: inline-block;
    width: 50px;
    height: 50px;
    border: 1px solid #ddd;
    text-align: center;
    line-height: 50px;
    cursor: pointer;
  }
  .selected {
    background-color: #3498db;
    color: #fff;
  }
  </style>