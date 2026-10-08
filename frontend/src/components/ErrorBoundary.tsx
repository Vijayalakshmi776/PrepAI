import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';
import { Button } from './ui/Button';

interface Props {
  children: ReactNode;
  fallbackMessage?: string;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('[PrepAI ErrorBoundary Captured Exception]', error, errorInfo);
  }

  private handleReset = () => {
    this.setState({ hasError: false, error: null });
    window.location.reload();
  };

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-[400px] flex items-center justify-center p-6">
          <div className="max-w-md w-full rounded-[2rem] border border-rose-200 bg-white p-8 shadow-soft text-center">
            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-rose-100 text-rose-600">
              <AlertTriangle className="h-7 w-7" />
            </div>
            <h2 className="mt-4 text-xl font-bold text-slate-950">Something went wrong</h2>
            <p className="mt-2 text-xs text-slate-600 leading-relaxed">
              {this.props.fallbackMessage || 'An unexpected rendering error occurred. The application recovered safely.'}
            </p>
            {this.state.error && (
              <div className="mt-4 rounded-xl bg-slate-50 p-3 text-[11px] font-mono text-slate-700 text-left overflow-x-auto border border-slate-200">
                {this.state.error.toString()}
              </div>
            )}
            <div className="mt-6 flex items-center justify-center gap-3">
              <Button onClick={this.handleReset} className="inline-flex items-center gap-2">
                <RefreshCw className="h-4 w-4" /> Reload Page
              </Button>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
