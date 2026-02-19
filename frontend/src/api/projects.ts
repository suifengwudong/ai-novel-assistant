import axios from 'axios'

const api = axios.create({ baseURL: '/api/v1', timeout: 30000 })

export interface NovelProject {
  id: string
  title: string
  description?: string
  genre?: string
  status: 'draft' | 'published' | 'archived'
  content?: string
  word_count: number
  created_at: string
  updated_at: string
  user_id?: string
}

export interface ProjectCreate {
  title: string
  description?: string
  genre?: string
  content?: string
  status?: string
}

export interface ProjectUpdate {
  title?: string
  description?: string
  genre?: string
  content?: string
  status?: string
}

export const getProjects = (status?: string) =>
  api.get<NovelProject[]>('/projects', { params: status ? { status } : {} }).then(r => r.data)

export const getProject = (id: string) =>
  api.get<NovelProject>(`/projects/${id}`).then(r => r.data)

export const createProject = (body: ProjectCreate) =>
  api.post<NovelProject>('/projects', body).then(r => r.data)

export const updateProject = (id: string, body: ProjectUpdate) =>
  api.put<NovelProject>(`/projects/${id}`, body).then(r => r.data)

export const deleteProject = (id: string) =>
  api.delete(`/projects/${id}`)

export const exportProject = async (id: string, format: 'markdown' | 'pdf' | 'epub', title: string) => {
  const res = await api.post(`/export/projects/${id}/${format}`, {}, { responseType: 'blob' })
  const ext = format === 'markdown' ? 'md' : format
  const url = URL.createObjectURL(res.data)
  const a = document.createElement('a')
  a.href = url
  a.download = `${title}.${ext}`
  a.click()
  URL.revokeObjectURL(url)
}
