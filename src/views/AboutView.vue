<template>
  <div>
    <div class="cont1" style="text-align: center">
      <table>
        <caption id="a"><h2>Conference Rooms</h2></caption>
        <tr>
          <th>Room Name</th>
          <th>Department</th>
          <th>Type</th>
          <th>Location</th>
          <th>Date</th>
          <th>Start Time</th>
          <th>End Time</th>
          <th>Max Duration</th>
          <th>Operation</th>
        </tr>
        <tbody id="tbody" style="display: none">
        <tr v-for="(room, index) in rooms" :key="index">
          <td>{{ room.name }}</td>
          <td>{{ room.department }}</td>
          <td>{{ room.type }}</td>
          <td>{{ room.location }}</td>
          <td>{{ room.date }}</td>
          <td>{{ room.startTime }}</td>
          <td>{{ room.endTime }}</td>
          <td>{{ room.maxDuration }}</td>
          <td>
            <button @click="deleteRoom(index)">Delete</button>
            <button @click="editRoom(room)">Edit</button>
          </td>
        </tr>
        </tbody>
      </table>

      <button @click="showPopup">Add Room</button>

    </div>

    <div >
      <form >
        <div >
          <label for="department">
            Department Name
          </label>
          <input
              id="department"
              type="text"
              placeholder="Enter department name"
          />
        </div>
        <div >
          <label for="room"> Room Name </label>
          <input
              id="room"
              type="text"
              placeholder="Enter room name"
          />
        </div>
        <div >
          <label for="date">
            Date (YYYY/MM/DD)
          </label>
          <input

              id="date"
              type="text"
              placeholder="YYYY/MM/DD"
          />
        </div>
        <div>
          <label> Room Type </label>
          <div>
            <label >
              <input type="radio" name="roomType" value="small" />
              <span class="ml-2">Small</span>
            </label>
            <label>
              <input type="radio" name="roomType" value="medium" />
              <span class="ml-2">Medium</span>
            </label>
            <label>
              <input type="radio" name="roomType" value="big" />
              <span class="ml-2">Big</span>
            </label>
          </div>
        </div>
        <div >
          <label for="startTime"> Start Time </label>
          <input

              id="startTime"
              type="text"
              placeholder="HH:MM"
          />
        </div>
        <div>
          <label for="endTime"> End Time </label>
          <input

              id="endTime"
              type="text"
              placeholder="HH:MM"
          />
        </div>
        <div>
          <label> Location </label>
          <select

              id="location"
          >
            <option>Teaching Building No.1 Lecture Hall</option>
            <option>Research Building Lecture Hall</option>
            <option>Library Conference Hall</option>
            <option>South Building</option>
          </select>
        </div>
        <div >
          <label for="roomNumber">
            Room Number
          </label>
          <input

              id="roomNumber"
              type="text"
              placeholder="Enter room number"
          />
        </div>
        <div>
          <label for="duration">
            Duration (in hours)
          </label>
          <input
              id="duration"
              type="number"
              placeholder="Enter duration"
          />
        </div>
        <div >
          <button
              type="button"
          >
            Submit
          </button>
        </div>
      </form>
    </div>



  </div>
</template>

<script>
export default {
  data() {
    return {

    };

  },
  methods: {
  }
}
</script>

<style scoped>
/* 设置全局样式 */
body {

  background-repeat:no-repeat;
  font-family: Arial, sans-serif;
  background-color: #f2f2f2;
  margin: 0;
  padding: 0;
}

/* 设置标题样式 */
h2 {
  color: #333;
}

/* 设置页面容器样式 */
.cont1 {
  opacity: 0.7;
  text-align: center;
  background-color: #fff;
  margin: 20px;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  border-radius: 5px;
}

/* 设置表格样式 */
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

table, th, td {
  border: 1px solid #ccc;
}

th, td {
  padding: 10px;
  text-align: center;
}

th {
  background-color: #333;
  color: #fff;
}

/* 设置按钮样式 */
button {
  background-color: #333;
  color: #fff;
  border: none;
  padding: 10px 20px;
  margin-top: 10px;
  border-radius: 5px;
  cursor: pointer;
}

/* 设置弹窗样式 */
#overlay {
  text-align: center;
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  z-index: 1;
}

.popup {

  background-repeat:no-repeat;
  background-color: #fff;
  width: 700px;
  padding: 20px;
  margin: 100px auto;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

/* 设置表格行样式 */
tbody tr:nth-child(odd) {
  background-color: #f2f2f2;
}

/* 设置编辑弹窗样式 */
#editOverlay {
  text-align: center;
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  z-index: 1;
}

#editOverlay .popup {
  background-color: #fff;
  width: 700px;
  padding: 20px;
  margin: 100px auto;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

/* 设置表格输入字段样式 */
input[type="text"],
input[type="number"],
select {
  width: 40%;
  padding: 10px;
  margin: 5px 0;
  border: 1px solid #ccc;
  border-radius: 3px;
}

/* 设置表格操作按钮样式 */
input[type="button"] {
  background-color: #333;
  color: #fff;
  border: none;
  padding: 10px 20px;
  margin: 5px;
  border-radius: 5px;
  cursor: pointer;
}
</style>
