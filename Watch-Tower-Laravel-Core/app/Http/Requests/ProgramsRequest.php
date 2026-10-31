<?php

namespace App\Http\Requests;

use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Foundation\Http\FormRequest;

class ProgramsRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    /**
     * @return array<string, ValidationRule|array<mixed>|string>
     */
    public function rules(): array
    {
        $creating = $this->isMethod('post');

        return [
            'program_name' => [$creating ? 'required' : 'sometimes', 'string', 'max:200'],
            'program_url' => ['nullable', 'url', 'max:500'],
            'scopes' => ['sometimes', 'array', 'max:5000'],
            'scopes.*' => ['string', 'max:500'],
            'out_of_scope' => ['sometimes', 'array', 'max:5000'],
            'out_of_scope.*' => ['string', 'max:500'],
            'meta' => ['sometimes', 'array'],
        ];
    }

    public function messages(): array
    {
        return [
            'program_name.required' => 'The program name is required.',
            'scopes.*.string' => 'Every in-scope asset must be a string.',
            'out_of_scope.*.string' => 'Every out-of-scope asset must be a string.',
        ];
    }
}
