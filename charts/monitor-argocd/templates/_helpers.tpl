{{- define "monitor-argocd.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "monitor-argocd.labels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{- define "monitor-argocd.image" -}}
{{- printf "%s:%s" .Values.image.repository .Values.image.tag | quote -}}
{{- end -}}

{{- define "monitor-argocd.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
{{- .Release.Name }}-{{ .Chart.Name }}-sa
{{- else -}}
{{- .Values.serviceAccount.name -}}
{{- end -}}
{{- end -}}