import { notFound } from 'next/navigation'
import { absolute } from '@/lib/url'
import AddNoteForm from './AddNoteForm'
import PutCustomFieldsForm from './PutCustomFieldsForm'
import CreateTaskInline from './CreateTaskInline'
import PresignAttachmentForm from './PresignAttachmentForm'

async function getAccount(id: string) {
  const url = await absolute(`/api/accounts/${id}`)
  const res = await fetch(url, { cache: 'no-store' })
  if (!res.ok) return null
  return res.json()
}

async function getNotes(id: string) {
  const url = await absolute(`/api/notes?entity_type=account&entity_id=${id}`)
  const res = await fetch(url, { cache: 'no-store' })
  const data = await res.json().catch(() => ({}))
  return data.items ?? []
}

async function getTasks(id: string) {
  const url = await absolute(`/api/tasks?assignee=&status=&entity_type=account&entity_id=${id}`)
  const res = await fetch(url, { cache: 'no-store' })
  const data = await res.json().catch(() => ({}))
  return data.items ?? []
}

async function getCFDefs() {
  const url = await absolute('/api/custom_fields/definitions')
  const res = await fetch(url, { cache: 'no-store' })
  const data = await res.json().catch(() => ({}))
  return data.items ?? []
}

async function getCFValues(id: string) {
  const url = await absolute(`/api/custom_fields/values?entity_type=account&entity_id=${id}`)
  const res = await fetch(url, { cache: 'no-store' })
  const data = await res.json().catch(() => ({}))
  return data.values ?? {}
}

export default async function AccountDetail({ params }: { params: { id: string } }) {
  const acct = await getAccount(params.id)
  if (!acct) return notFound()
  const [notes, tasks, defs, values] = await Promise.all([
    getNotes(params.id),
    getTasks(params.id),
    getCFDefs(),
    getCFValues(params.id),
  ])
  const accountDefs = defs.filter((d: any) => d.entity_type === 'account')
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">{acct.name}</h1>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card p-4">
          <h2 className="font-semibold mb-2">ノート</h2>
          <ul className="list-disc ml-5">
            {notes.map((n: any) => (
              <li key={n.id}>{n.body}</li>
            ))}
            {notes.length === 0 && <li>ノートがありません</li>}
          </ul>
          {/* @ts-expect-error Server/Client boundary */}
          <AddNoteForm entityType="account" entityId={params.id} />
        </div>

        <div className="card p-4">
          <h2 className="font-semibold mb-2">タスク</h2>
          <ul className="list-disc ml-5">
            {tasks.map((t: any) => (
              <li key={t.id}>{t.title} ({t.status})</li>
            ))}
            {tasks.length === 0 && <li>タスクがありません</li>}
          </ul>
          {/* @ts-expect-error Server/Client boundary */}
          <CreateTaskInline entityType="account" entityId={params.id} />
        </div>

        <div className="card p-4">
          <h2 className="font-semibold mb-2">カスタムフィールド</h2>
          {/* @ts-expect-error Server/Client boundary */}
          <PutCustomFieldsForm entityId={params.id} defs={accountDefs} initialValues={values} />
        </div>

        <div className="card p-4">
          <h2 className="font-semibold mb-2">添付ファイル（プリサインURL）</h2>
          {/* @ts-expect-error Server/Client boundary */}
          <PresignAttachmentForm entityType="account" entityId={params.id} />
          <p className="text-xs text-gray-500 mt-2">アップロード自体はスタブです。返却された upload_url / object_url を用いて将来S3に置き換え可能です。</p>
        </div>
      </div>
    </div>
  )
}
