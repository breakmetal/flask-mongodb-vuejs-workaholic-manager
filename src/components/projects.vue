<template>
  <v-data-table
    :headers="headers"
    :items="projects"
    sort-by="calories"
    class="elevation-1"
  >
    <template v-slot:top>
      <v-toolbar flat color="white">
        <v-toolbar-title>My projects</v-toolbar-title>
        <v-divider
          class="mx-4"
          inset
          vertical
        ></v-divider>
        <div class="flex-grow-1"></div>
        <v-dialog v-model="dialog" max-width="500px">
          <template v-slot:activator="{ on }">
            <v-btn color="primary" dark class="mb-2" v-on="on">New Project</v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="headline">{{ formTitle }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field v-model="editedItem.title" label="title"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field v-model="editedItem.description" label="description"></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <div class="flex-grow-1"></div>
              <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
              <v-btn color="blue darken-1" text @click="save">update</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <template v-slot:item.action="{ item }">
        <v-icon
        small
        class="mr-2"
        @click="viewItem(item)"
      >
        mdi-eye
      </v-icon>
      <v-icon
        small
        class="mr-2"
        @click="editItem(item)"
      >
       mdi-pencil
      </v-icon>
      <v-icon
        small
        @click="deleteItem(item)"
      >
        mdi-delete-forever
      </v-icon>
    </template>
    <template v-slot:no-data>
      <v-btn color="primary" @click="getProjects">Reset</v-btn>
    </template>
  </v-data-table>
</template>

<script>
import axios from 'axios'
  export default {
    data: () => ({
      dialog: false,
      headers: [
        {
          text: 'Title',
          align: 'left',
          sortable: true,
          value: 'title',
        },
        { text: 'Description', value: 'description'},
        { text: 'Actions', value: 'action', sortable: false },
      ],
      projects: [],
      editedIndex: -1,
      editedItem: {
        title: '',
        description: ''
      },
      defaultItem: {
        name: '',
        calories: 0,
        fat: 0,
        carbs: 0,
        protein: 0,
      },
    }),
    computed: {
      formTitle () {
        return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
      },
    },
    watch: {
      dialog (val) {
        val || this.close()
      },
    },
    created () {
      this.getProjects()
    },
    methods: {
        getProjects () {
            axios({ method: 'GET', url: 'http://127.0.0.1:5000/api/list_projects' }).then(
                result => {
                            console.log(result.data)
                            this.projects = result.data
                },
            error => {
                console.error(error)
            })
        },
        editItem (item) {
            this.editedIndex = this.projects.indexOf(item)
            this.editedItem = Object.assign({}, item)
            this.dialog = true
        },
      deleteItem (item) {
        this.editedItem = Object.assign({}, item)
        this.id = this.editedItem._id.$oid
        axios({ method: 'DELETE', url: `http://127.0.0.1:5000/api/delete_project/${this.id}` }).then(
                result => {
                            console.log(result.data)
                            this.getProjects()

                },
            error => {
                console.error(error)
            })
      },
      viewItem(item) {
          this.$router.push('/project-view')
      },
      close () {
        this.dialog = false
        setTimeout(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        }, 300)
      },
      save () {
        if (this.editedIndex == -1) {
          axios.post(`http://127.0.0.1:5000/api/add_project`,this.editedItem).then(
            result => {
                this.isEdit = false
                this.getProjects()
                console.log(result)
          }).catch(err => {
              console.log(err)
          })
        } else {
          this.id = this.editedItem._id.$oid
          axios.put(`http://127.0.0.1:5000/api/update_project/${this.id}`,this.editedItem).then(
            result => {
                this.isEdit = false
                this.getProjects()
                console.log(result)
        }).catch(err => {
            console.log(err)
        })

        }

        this.close()
      },
    },
  }
</script>