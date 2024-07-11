import { defineStore } from "pinia"
import { getData, postData } from "../utils/http-requests"
import { getTodaysDate } from "../utils/misc.js"
import { GlobalState, ServerResponse, Project, User, Product } from "../interfaces/interfaces"

export const useAuthStore = defineStore("auth", {
  state: (): GlobalState => ({
    isLoggedIn: false,
    user: null,
    projects: [],
    currentProject: null,
  }),
  actions: {
    // Handle User state
    logIn(user): boolean {
      console.log(user)
      this.isLoggedIn = true
      this.user = user
      this.projects = user.projects
      return true
    },
    async logOut(): Promise<void> {
      console.log("logOut called")
      const response: ServerResponse = await postData({}, "/logout")
      console.log("server response: ", response)

      if (response.status === "success") {
        this.isLoggedIn = false
        this.user = null
        this.projects = []
        this.currentProject = null
      }
    },
    async checkSession(): Promise<void> {
      const response: ServerResponse = await getData("/session")

      if (response.status === "success") {
        this.isLoggedIn = true
        this.user = response
        this.projects = response.projects
      } else {
        this.isLoggedIn = false
        this.user = null
      }
    },

    // Handle Project state
    setCurrentProject(project: Project): void {
      this.currentProject = project
      console.log("setCurrentProject: ", this.currentProject.name)
      console.log(this.currentProject)
    },
    pushToProjects(project: Project): void {
      this.projects.push(project)
    },
    popFromProjects(project_id: number): void {
      console.log(`popFromProjects called for id: ${project_id}`)
      if (this.currentProject?.project_id === project_id) {
        this.currentProject = null
      }

      this.projects = this.projects.filter((p) => p.project_id !== project_id)
    },

    // Handle Product state
    pushToProducts(product: Product): void {
      console.log(`pushToProducts called for id: ${product.product_id}`)
      if (this.currentProject) {
        this.currentProject.products.push(product)
        this.currentProject.updated_date = getTodaysDate()
      }
    },
    popFromProducts(product_id: number): void {
      console.log(`popFromProducts called for id: ${product_id}`)
      if (!this.currentProject) return

      this.currentProject.products = this.currentProject.products.filter(
        (p) => p.product_id !== product_id
      )
      this.currentProject.updated_date = getTodaysDate()
    },
  },
})
